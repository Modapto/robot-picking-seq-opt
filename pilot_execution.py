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
from exact_method import *
from method_linear import *
from pilot_preprocessing import *
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

def run_tsp(json_file_path=None, input_data=None, generate_new_instance=False):
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

    output_data = {
        "produced_at": int(time() * 1000),
        "data": {
            "optimization_run": is_valid,
            "message": validation_msg,
            "solutionTime": (int(time() * 1000) - solution_time_start),
            "totalTime": (int(time() * 1000) - total_time_start),
        }
    }

    if is_valid:
        output_data["data"]["optimization_results"] = results

    with open("pilot_execution_output.json", 'w') as json_file:
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
