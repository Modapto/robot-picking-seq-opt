import json
import copy
import traceback
from datetime import datetime
from time import *
import pika
import sys
import pandas as pd
import numpy as np
from co_GraphCreation import *
from co_exact_method import *
from co_method_linear import *
from co_pilot_opt_preprocessing import *
import base64
import pickle

online = sys.argv[1]  # This argument will differentiate between local and remote runs

# Function to convert data types to native Python types (e.g., for JSON serialization)
def convert_to_native_types(data):
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

    # ✅ Component availability validation
    is_valid, validation_msg = validate_component_availability(
        data.get("kh_sequences") or [[data.get("kh_setup", [])]],
        data["kit_holders_template"],
        data["containers_template"]
    )

    if not is_valid:
        validation_msg = validation_msg
    else:
        validation_msg = "Valid KH sequence optimization starts..."


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

    decoded_path = "co_pilot_opt_execution_output.json"
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

    encoded_path = "co_encoded_opt_output.json"
    with open(encoded_path, "w") as f_enc:
        json.dump(wrapper, f_enc, indent=4)
    print(f"Encoded result written to {encoded_path}")

    return output_data
