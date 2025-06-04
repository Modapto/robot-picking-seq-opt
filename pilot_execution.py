import json
import copy
import traceback
from datetime import datetime
from time import *
import pika
import sys
import pandas as pd
import numpy as np
from instances_generator import *
from parse_json import *
from GraphCreation import *
from heuristic_methods import *
from reinforcement_learning import *
from exact_method import *
from rl_heuristics import *
from method_linear import *
# from simulator import *
# from simulator_v2 import *

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

def generate_kh_configuration1(input_data):
    if isinstance(input_data, str):
        with open(input_data, 'r') as f:
            input_data = json.load(f)

    try:
        kh_sequences = input_data["data"]["kh_sequences"]
        print("Loaded kh_sequences:", kh_sequences)  # <-- 🔍 DEBUG PRINT HERE

        assert isinstance(kh_sequences, list)
        assert all(isinstance(k, dict) for k in kh_sequences)
        return kh_sequences
    except Exception as e:
        raise ValueError(f"Invalid or missing 'kh_sequences' in JSON: {e}")


def extract_gr_nodes_from_sequence(gr_sequence, containers_template):
    gr_nodes = {}  # e.g., { "1.5.1": "Component_10" }
    for entry in gr_sequence:
        for gr_pos, container_id in entry.items():  # "GRPos_1.5": "Container_5"
            base_pos = gr_pos.split("_")[1]  # → "1.5"
            contents = containers_template.get(container_id, {}).get("contents", [])
            for comp in contents:
                comp_type = comp["type"]
                sub_pos = comp["position"]  # → "1", "2", etc.
                full_gr_node = f"{base_pos}.{sub_pos}"  # → "1.5.1"
                gr_nodes[full_gr_node] = comp_type
    return gr_nodes

def extract_kh_nodes_from_sequence(kh_config, kit_holders_template):
    kh_nodes = {}  # e.g., { "KHPos_1": ["Component_1", "Component_2"] }
    for pos in kh_config:  # e.g., {'KHPos_1': 'KH001'}
        for pos_key, kh_id in pos.items():
            contents = kit_holders_template.get(kh_id, {}).get("contents", [])
            kh_nodes[pos_key] = [item["type"] for item in contents]
    return kh_nodes

def filter_distance_matrix(distance_matrix, kh_gr_config):
    """
    Filters the distance matrix based on KH and GR nodes,
    and returns it in the format expected by create_distance_matrices().
    """

    assert isinstance(kh_gr_config, list), "kh_gr_config must be a list of dictionaries."
    assert all(isinstance(k, dict) for k in kh_gr_config), "Each item in kh_gr_config must be a dictionary."

    used_kh_nodes = set()
    for kh_setup in kh_gr_config:
        for kh_pos, kh_id in kh_setup.items():
            used_kh_nodes.add(kh_pos.replace("KHPos_", ""))

    used_gr_nodes = set()
    for from_node in distance_matrix:
        if from_node.startswith("GRPos_"):
            used_gr_nodes.add(from_node.replace("GRPos_", ""))
    for neighbors in distance_matrix.values():
        for to_node in neighbors:
            if to_node.startswith("GRPos_"):
                used_gr_nodes.add(to_node.replace("GRPos_", ""))

    filtered_matrix = []
    for from_node, neighbors in distance_matrix.items():
        from_clean = from_node.replace("GRPos_", "").replace("KHPos_", "")
        for to_node, dist in neighbors.items():
            to_clean = to_node.replace("GRPos_", "").replace("KHPos_", "")
            if (
                (from_clean in used_gr_nodes and to_clean in used_kh_nodes)
                or (from_clean in used_kh_nodes and to_clean in used_gr_nodes)
                or (from_clean in ["0.0", "0.0.0"] or to_clean in ["0.0", "0.0.0"])
            ):
                filtered_matrix.append({
                    "edge": f"({from_clean}, {to_clean})",
                    "distance": dist
                })

    print(f"  ➤ Filtered matrix has {len(filtered_matrix)} edges.")
    return {"distanceMatrix": filtered_matrix}


def run_tsp(json_file_path=None, input_data=None, generate_new_instance=False):
    from time import time
    import json

    solution_time_start = int(time() * 1000)
    total_time_start = int(time() * 1000)

    # Load input data
    if input_data and "data" in input_data:
        print("Remote input data received.")
        data = input_data["data"]
    elif json_file_path:
        with open(json_file_path, 'r') as f:
            input_data = json.load(f)
        data = input_data["data"]
        print(f"Local JSON input has been loaded from {json_file_path}.")
    else:
        raise ValueError("Input data is required, either via JSON file or directly.")

    distance_matrix = data["distance_matrix"]
    gr_sequence = data["gr_sequence"]
    kh_sequences = data["kh_sequences"]
    containers = data["containers_template"]
    kit_holders = data["kit_holders_template"]

    # Build detailed GR nodes like GRPos_1.5.1, GRPos_1.5.2, etc.
    gr_positions = []
    for gr_dict in gr_sequence:
        for gr_pos, container_id in gr_dict.items():
            contents = containers[container_id]["contents"]
            for item in contents:
                index = item["position"]
                gr_positions.append(f"{gr_pos}.{index}")

    start_node = "0.0"
    end_node = "0.0"

    results = []
    for i, kh_config in enumerate(kh_sequences):
        print(f">>> Running Phase {i + 1} with KH Setup: {kh_config}")

        # Prepare current kit holder config
        current_kh_config = {}
        for pos in kh_config:
            for pos_key, kh_id in pos.items():
                current_kh_config[pos_key] = kit_holders[kh_id]

        config = generate_kh_configuration1(input_data)
        print(">>> Running Phase 1 with KH Setup:", config)

        filtered_matrix = filter_distance_matrix(distance_matrix, config)

        print(f"  ➤ GR nodes: {len(gr_positions)} | Sample: {gr_positions[:20]}")
        print(f"  ➤ KH nodes: {len(current_kh_config)} | Sample: {list(current_kh_config.keys())[:20]}")
        print(f"  ➤ Filtered matrix has {len(filtered_matrix)} edges.")

        a_to_b_matrix = create_distance_matrices1({"data": {"distance_matrix": filtered_matrix}})

        B, set_1, set_2 = create_directed_bipartite_graph(a_to_b_matrix)

        print(f"  ➤ Directed graph created with {len(B.nodes)} nodes and {len(B.edges)} edges.")

        method = data["method"]
        phase_results = {}

        if method in ["exact", "exact-linear"]:
            exact_input = {
                "data": {
                    "distanceMatrix": filtered_matrix,
                    "start_node": start_node,
                    "end_node": end_node if i == len(kh_sequences) - 1 else None
                }
            }
            exact_tour, exact_tour_cost, time_details_exact = run_exact_tsp(exact_input)
            if i < len(kh_sequences) - 1:
                for j in range(len(exact_tour) - 1, -1, -1):
                    if exact_tour[j][1] == "0.0.0":
                        exact_tour = exact_tour[:j]
                        break
                time_details_exact = [step for step in time_details_exact if step["to"] not in ["0.0.0", "0.0"]]
                exact_tour_cost = sum(step["distance"] for step in time_details_exact)
            phase_results["exact"] = {"cost": exact_tour_cost, "time_details": time_details_exact}

        if method in ["linear", "exact-linear"]:
            linear_tour = linear_picking(B, start_node, end_node, set_1, set_2, filtered_matrix=filtered_matrix)
            linear_tour_cost, time_details_linear = total_cost(B, linear_tour['tour'], filtered_matrix=filtered_matrix)
            if i < len(kh_sequences) - 1:
                for j in range(len(linear_tour['tour']) - 1, -1, -1):
                    if linear_tour['tour'][j] == "0.0.0":
                        linear_tour['tour'] = linear_tour['tour'][:j]
                        break
                time_details_linear = [step for step in time_details_linear if step["to"] not in ["0.0.0", "0.0"]]
                linear_tour_cost = sum(step["totalTime"] for step in time_details_linear)
            phase_results["linear"] = {"cost": linear_tour_cost, "time_details": time_details_linear}

        if method == "exact-linear":
            if exact_tour_cost is not None and linear_tour_cost is not None:
                improvement = round(((linear_tour_cost - exact_tour_cost) / linear_tour_cost) * 100, 4)
                if improvement > 0:
                    phase_results = {"exact": phase_results["exact"], "improvement_percentage": improvement}
                else:
                    phase_results = {"linear": phase_results["linear"], "improvement_percentage": improvement}

        results.append(phase_results)

    output_data = {
        "produced_at": int(time() * 1000),
        "data": {
            "phases": results,
            "solutionTime": (int(time() * 1000) - solution_time_start),
            "totalTime": (int(time() * 1000) - total_time_start),
        }
    }

    with open("output_tsp_results.json", 'w') as json_file:
        json.dump(convert_to_native_types(output_data), json_file, indent=4)

    return output_data

def callback(ch, method, properties, body):
    input_file = json.loads(body)
    uuid = input_file['uuid']
    data = input_file['data']

    try:
        print("%s: Job with uuid: %s received" % (datetime.now().strftime("%d/%m/%Y %H:%M:%S"), uuid))
        input_postman_file_path = "input_postman.json"
        output_postman_file_path = "output_postman.json"
        #Run the TSP algorithm for the JSON input
        if data.get("method") == "simulation":
            output = run_simulation(input_file)
        else:
            output = run_tsp(None, input_file, False)

        print("%s: Publishing results to queue." % (datetime.now().strftime("%d/%m/%Y %H:%M:%S")))

        output = json.dumps(output)
        channel.basic_publish(exchange='opt-result', routing_key='robot-picking-seq', body=output)
        print("%s: Job with uuid: %s completed" % (datetime.now().strftime("%d/%m/%Y %H:%M:%S"), uuid))
    except Exception as e:
        #print(Exception, e)
        print(traceback.format_exc())
        error_message = {"message": "Problem in input data: " + str(e)}
        error_responce = {"uuid": uuid, "data": error_message, "produced_at": int(time() * 1000)}
        error_responce = json.dumps(error_responce)
        channel.basic_publish(exchange='opt-result', routing_key='robot-picking-seq', body=error_responce)
        print("%s: Job with uuid: %s failed" % (datetime.now().strftime("%d/%m/%Y %H:%M:%S"), uuid))


# Main Execution
if online == "1":  # Remote mode with RabbitMQ
    host = sys.argv[2]
    port = sys.argv[3]
    username = sys.argv[4]
    password = sys.argv[5]
    credentials = pika.PlainCredentials(username, password)
    params = pika.ConnectionParameters(host, port, '/', credentials, heartbeat=1860, blocked_connection_timeout=930)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.basic_consume(queue='robot-picking-seq_job', auto_ack=True, on_message_callback=callback)
    channel.start_consuming()

elif online == "0":  # Local mode with JSON file input
    filename = sys.argv[2]
    with open(filename, 'r') as f:
        input_data = json.load(f)

    if input_data["data"]["method"] == "simulation":
        print("Running simulation...")
        run_simulation(input_data)
    else:
        print("Running optimization...")
        run_tsp(json_file_path=filename, input_data=None, generate_new_instance=False)
