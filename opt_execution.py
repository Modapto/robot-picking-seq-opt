# REPOSITORY NAME (c) by the University of Piraues, Greece.
#
# REPOSITORY NAME is licensed under a
# Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <http://creativecommons.org/licenses/by-nc-nd/3.0/>.

import json
import copy
import traceback
from datetime import datetime
from time import *
import pika
import sys
import pandas as pd
import numpy as np
from parse_json import *
from graph_creation import *
from heuristic_methods import *
from reinforcement_learning_method import *
from exact_method import *
from linear_method import *
from opt_preprocessing import *
import base64
import pickle

online = sys.argv[1]  # This argument will differentiate between local and remote runs

def convert_to_native_types(data):
    """
    Recursively convert data to JSON-serializable native Python types.
    """
    if isinstance(data, dict):
        return {k: convert_to_native_types(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_to_native_types(v) for v in data]
    elif isinstance(data, pd.DataFrame):
        return data.applymap(lambda x: int(x) if isinstance(x, (np.integer, np.int32, np.int64)) else x).to_dict()
    elif isinstance(data, (np.integer, np.int32, np.int64)):
        return int(data)
    else:
        return data

def run_tsp(json_file_path=None, input_data=None, generate_new_instance=False):
    """
     Run the TSP-based optimization for pick-and-place operations.

     The function can be called in two ways:
         - With a JSON file path (local mode),
         - With a pre-decoded `input_data` dict (remote/service mode).

     It:
         - Parses and validates the input,
         - Builds or loads distance matrices and graphs,
         - Executes one or more optimization methods
           (nearest, 2-opt, exact, q-learning, linear, exact-linear, etc.),
         - Collects costs, tours, and time details,
         - Serializes results both in plain JSON and in base64-encoded form.

     Parameters:
         json_file_path (str or None): Path to a JSON file containing wrapped input data.
         input_data (dict or None): Already-decoded input dictionary as received from a caller.
         generate_new_instance (bool): Reserved flag (currently unused) for instance generation.
     """
    solution_time_start = int(time() * 1000)
    total_time_start = int(time() * 1000)

    if input_data and "data" in input_data:
        print("run_tsp received pre-decoded input.")
        msg  = input_data               # already plain
        data = msg["data"]

    elif json_file_path:
        with open(json_file_path) as f:
            msg = json.load(f)
        # unwrap possible base64
        if isinstance(msg["data"], dict) and "base64" in msg["data"]:
            raw = base64.b64decode(msg["data"]["base64"])
            try:
                msg["data"] = pickle.loads(raw)
            except pickle.UnpicklingError:
                msg["data"] = json.loads(raw.decode())
        data = msg["data"]
        print(f"Local JSON input loaded from {json_file_path}.")

    else:
        raise ValueError("run_tsp needs either json_file_path or input_data")

    raw_distance_matrix = input_data["data"]["distance_matrix"]
    container_types = input_data["data"]["containers_template"]
    kit_holder_types = input_data["data"]["kit_holders_template"]
    kh_sequences = input_data["data"]["kh_sequences"]
    gr_sequence = input_data["data"]["gr_sequence"]
    start_node = "0.0"
    end_node = "0.0"

    #Component availability validation
    is_valid, validation_msg = validate_component_availability(
        data.get("kh_sequences") or [[data.get("kh_setup", [])]],
        data["kit_holders_template"],
        data["containers_template"]
    )

    if not is_valid:
        validation_msg = validation_msg
    else:
        validation_msg = "Valid KH sequence optimization starts..."

    method = data["method"]

    # ===================== COMPLETE GRAPH MODE =====================
    if method in ["nearest_complete", "2opt_complete", "exact_complete", "qlearning_complete", "all_complete"]:
        print(f"Running COMPLETE GRAPH mode with method = {method}")

        distance_matrix_opt = data.get("distance_matrix_opt")
        if distance_matrix_opt is None:
            raise ValueError("distance_matrix_opt is required for *_complete methods")

        # you can override these via JSON if you want
        start_node_complete = data.get("start_node", "0.0")
        end_node_complete = data.get("end_node", "0.0.0")

        complete_input = {
            "data": {
                "distanceMatrix": distance_matrix_opt,
                "start_node": start_node_complete,
                "end_node": end_node_complete,
            }
        }

        a_to_b_matrix = create_distance_matrices(complete_input)
        print("Distance matrices (complete graph) created.")
        B, set_1, set_2 = create_directed_bipartite_graph(a_to_b_matrix)
        print(f"  ➤ COMPLETE graph created with {len(B.nodes)} nodes and {len(B.edges)} edges.")

        # this dict will go into output_data["optimization_results"]
        results = {}

        # ---------- Nearest Neighbor ----------
        if method in ["nearest_complete", "2opt_complete", "all_complete"]:
            try:
                print("Running Nearest Neighbor (complete graph)...")
                start_time_nearest = int(time() * 1000)

                nn_tour = nearest_tsp(B, start_node_complete, end_node_complete, set_1, set_2)
                nn_cost, nn_time_details = total_cost(B, nn_tour)

                exec_time_nearest = int(time() * 1000) - start_time_nearest

                results["nearest"] = {
                    "tour": nn_tour,
                    "cost": nn_cost,
                    "exec_time": exec_time_nearest,
                    "time_details": nn_time_details
                }
                print(f"Nearest Neighbor (complete graph) cost: {nn_cost}")
            except Exception as e:
                print(f"Error in nearest_complete: {e}")
                results["nearest"] = {
                    "tour": [],
                    "cost": None,
                    "exec_time": None,
                    "time_details": f"Error: {e}"
                }

        # ---------- 2-opt ----------
        if method in ["2opt_complete", "all_complete"]:
            try:
                print("Running 2-opt (complete graph)...")
                start_time_2opt = int(time() * 1000)

                # initial tour: use nearest if available, otherwise compute once
                if "nearest" in results and results["nearest"]["tour"]:
                    simple_tour = results["nearest"]["tour"]
                    simple_cost = results["nearest"]["cost"]
                else:
                    simple_tour = nearest_tsp(B, start_node_complete, end_node_complete, set_1, set_2)
                    simple_cost, _ = total_cost(B, simple_tour)

                opt_tour, _ = two_opt_for_bipartite(simple_tour, B, set_1, set_2, max_iterations=1000)
                opt_cost, opt_time_details = total_cost(B, opt_tour)

                exec_time_2opt = int(time() * 1000) - start_time_2opt

                results["2-opt"] = {
                    "tour": opt_tour,
                    "cost": opt_cost,
                    "exec_time": exec_time_2opt,
                    "time_details": opt_time_details
                }
                print(f"2-opt (complete graph) cost: {opt_cost}")
            except Exception as e:
                print(f"Error in 2opt_complete: {e}")
                results["2-opt"] = {
                    "tour": [],
                    "cost": None,
                    "exec_time": None,
                    "time_details": f"Error: {e}"
                }

        # ---------- Exact ----------
        if method in ["exact_complete", "all_complete"]:
            try:
                print("Running Exact (complete graph)...")
                start_time_exact = int(time() * 1000)

                exact_tour, exact_cost, exact_time_details = run_exact_tsp(complete_input)
                exec_time_exact = int(time() * 1000) - start_time_exact

                results["exact"] = {
                    "tour": exact_tour,
                    "cost": exact_cost,
                    "exec_time": exec_time_exact,
                    "time_details": exact_time_details
                }
                print(f"Exact (complete graph) cost: {exact_cost}")
            except Exception as e:
                print(f"Error in exact_complete: {e}")
                results["exact"] = {
                    "tour": [],
                    "cost": None,
                    "exec_time": None,
                    "time_details": f"Error: {e}"
                }

        # ---------- Q-learning ----------
        if method in ["qlearning_complete", "all_complete"]:
            try:
                print("Running Q-learning (complete graph)...")
                start_time_q = int(time() * 1000)

                q_tour = q_learning_tsp(
                    B,
                    start_node_complete,
                    end_node_complete,
                    set_1,
                    set_2,
                    large_value=1000000,
                    episodes=2000  # adjust if you want more/less training
                )

                q_cost, q_time_details = total_cost(B, q_tour)
                exec_time_q = int(time() * 1000) - start_time_q

                results["qlearning"] = {
                    "tour": q_tour,
                    "cost": q_cost,
                    "exec_time": exec_time_q,
                    "time_details": q_time_details
                }
                print(f"Q-learning (complete graph) cost: {q_cost}")
            except Exception as e:
                print(f"Error in qlearning_complete: {e}")
                results["qlearning"] = {
                    "tour": [],
                    "cost": None,
                    "exec_time": None,
                    "time_details": f"Error: {e}"
                }

        # ---------- Build final output and return ----------
        output_data = {
            "optimization_run": is_valid,
            "message": validation_msg,
            "solutionTime": (int(time() * 1000) - solution_time_start),
            "totalTime": (int(time() * 1000) - total_time_start),
        }

        if is_valid:
            output_data["optimization_results"] = results

        decoded_path = "opt_execution_output.json"
        with open(decoded_path, "w") as f:
            json.dump(convert_to_native_types(output_data), f, indent=4)

        out_uuid = (input_data or {}).get("uuid") if input_data else msg.get("uuid", "no-uuid")
        wrapper = {
            "uuid": out_uuid,
            "produced_at": int(time() * 1000),
            "data": {
                "base64": base64.b64encode(pickle.dumps(output_data)).decode()
            }
        }
        encoded_path = "encoded_opt_output.json"
        with open(encoded_path, "w") as f_enc:
            json.dump(wrapper, f_enc, indent=4)
        print(f"Encoded result written to {encoded_path}")

        return output_data

    results = []
    # Step 1: Generate node maps
    gr_nodes = generate_gr_nodes(gr_sequence, container_types)
    kh_nodes = generate_kh_nodes(kh_sequences, kit_holder_types)

    # Step 2: Extend the distance matrix
    extended_matrix = extend_distance_matrix(gr_nodes, kh_nodes, raw_distance_matrix)

    # Step 3: Filter for optimization logic
    filtered_matrix = generate_filtered_distance_matrix(extended_matrix, gr_nodes, kh_nodes)
    a_to_b_matrix = create_distance_matrices({"data": {"distanceMatrix": filtered_matrix}})

    B, set_1, set_2 = create_directed_bipartite_graph(a_to_b_matrix)
    print(f"  ➤ Directed graph created with {len(B.nodes)} nodes and {len(B.edges)} edges.")

    method = data["method"]
    results = {}

    if method in ["exact", "exact-linear"]:
        exact_input = {
            "data": {
                "distanceMatrix": filtered_matrix,
                "start_node": start_node,
                "end_node": end_node
            }
        }
        exact_tour, exact_tour_cost, time_details_exact = run_exact_tsp(exact_input)
        annotated_time_details = annotate_component_in_time_details(time_details_exact, gr_nodes, kh_nodes)
        results["exact"] = {"cost": exact_tour_cost, "time_details": annotated_time_details}

    if method in ["linear", "exact-linear"]:
        linear_tour = linear_picking(B, start_node, end_node, set_1, set_2, filtered_matrix=filtered_matrix)
        linear_tour_cost, time_details_linear = total_cost(B, linear_tour['tour'], filtered_matrix=filtered_matrix)
        annotated_time_details = annotate_component_in_time_details(time_details_linear, gr_nodes, kh_nodes)
        results["linear"] = {"cost": linear_tour_cost, "time_details": annotated_time_details}

    if method == "exact-linear":
        if results["exact"]["cost"] is not None and results["linear"]["cost"] is not None:
            improvement = round(
                ((results["linear"]["cost"] - results["exact"]["cost"]) / results["linear"]["cost"]) * 100, 4)
            if improvement > 0:
                results = {"exact": results["exact"], "improvement_percentage": improvement}
            else:
                results = {"linear": results["linear"], "improvement_percentage": improvement}

    output_data =  {
            "optimization_run": is_valid,
            "message": validation_msg,
            "solutionTime": (int(time() * 1000) - solution_time_start),
            "totalTime": (int(time() * 1000) - total_time_start),
        }


    if is_valid:
        output_data["optimization_results"] = results

    decoded_path = "opt_execution_output.json"
    with open(decoded_path, "w") as f:
        json.dump(convert_to_native_types(output_data), f, indent=4)

    out_uuid = (input_data or {}).get("uuid") if input_data else msg.get("uuid", "no-uuid")
    wrapper = {
        "uuid": out_uuid,
        "produced_at": int(time() * 1000),
        "data": {
            "base64": base64.b64encode(pickle.dumps(output_data)).decode()
        }
    }

    encoded_path = "encoded_opt_output.json"
    with open(encoded_path, "w") as f_enc:
        json.dump(wrapper, f_enc, indent=4)
    print(f"Encoded result written to {encoded_path}")

    return output_data
