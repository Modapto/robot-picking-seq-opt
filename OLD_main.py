import json
import traceback
from datetime import datetime
from time import *
import pika
import sys
import pandas as pd
import numpy as np
from GraphCreation import *
from Solver import *
from instances_generator import *
from parse_json import *
from old_exact_method import *

online = sys.argv[1]

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

def run_tsp_for_size(json_file_path, output_json_file_path):
    total_time_start = int(time() * 1000)
    # generate the random JSON input
    random_json_input = generate_random_json_input()
    #save the JSON input to a file
    output_file_path = "random_json_input.json"
    with open(output_file_path, 'w') as json_file:
        json.dump(random_json_input, json_file, indent=4)

    print(f"JSON input has been saved to {output_file_path}")

    a_to_b_matrix, b_to_a_matrix = create_distance_matrices_from_json('random_json_input.json')
    print(a_to_b_matrix)
    print(b_to_a_matrix)
    print("Distance matrices created!")

    #create the bipartite graph
    B, set_1, set_2 = create_bipartite_graph(a_to_b_matrix, b_to_a_matrix)
    # plot_bipartite_graph(B)
    print("Graph generated!")

    with open(json_file_path, 'r') as f:
        input_data = json.load(f)

    start_node = input_data['data'].get('start_node', '0.0.0')
    end_node = input_data['data'].get('end_node', '0.0.0')
    method = input_data['data']['method']

    #adding the start/end node to the set_2 list explicitly
    if end_node not in set_2:
        set_2.append(end_node)

    results = {}
    solution_time_start = int(time() * 1000)
    simple_tour = None

    if method == "nearest" or method == "all":
        try:
            print("Running Nearest Neighbor TSP...")
            simple_tour = nearest_tsp(B, start_node, end_node, set_1, set_2)
            simple_tour_cost, time_details = total_cost(B, simple_tour)
            results["nearest"] = {
                "tour": simple_tour,
                "cost": simple_tour_cost,
                "time_details": time_details,
                "totalLoadingTime": simple_tour_cost
            }
            print(f"Nearest Neighbor TSP. Cost: {simple_tour_cost}")
        except ValueError as e:
            print(f"Error in nearest method: {e}")

    # 2-opt Optimization
    if method == "2-opt" or method == "all":
        try:
            print("Running 2-opt optimization...")
            # if nearest_tsp was not run before, generate the tour first
            if simple_tour is None:
                print("Nearest neighbor tour not found, generating it for 2-opt...")
                simple_tour = nearest_tsp(B, start_node, end_node, set_1, set_2)

            optimized_tour = opt2(simple_tour, B, set_1, set_2, start_node, end_node)
            optimized_tour_cost, time_details = total_cost(B, optimized_tour)
            results["2-opt"] = {
                "tour": optimized_tour,
                "cost": optimized_tour_cost,
                "time_details": time_details,
                "totalLoadingTime": optimized_tour_cost
            }
            print(f"2-opt TSP completed. Cost: {optimized_tour_cost}")
        except ValueError as e:
            print(f"Error in 2-opt method: {e}")

    if method == "q-learning" or method == "all":
        try:
            print("Running Q-Learning TSP...")
            q_learning_tour = q_learning_tsp(B, start_node, end_node, set_1, set_2)
            q_learning_tour_cost, time_details = total_cost(B, q_learning_tour)
            results["q-learning"] = {
                "tour": q_learning_tour,
                "cost": q_learning_tour_cost,
                "time_details": time_details,
                "totalLoadingTime": q_learning_tour_cost
            }
            print(f"Q-Learning TSP completed. Cost: {q_learning_tour_cost}")
        except ValueError as e:
            print(f"Error in q-learning method: {e}")

    # Exact Method TSP
    if method == "exact" or method == "all":
        try:
            print("Running Exact Method TSP...")

            # Call the exact TSP function from old_exact_method.py
            exact_tour, exact_tour_cost, time_details = run_exact_tsp_local(json_file_path)

            if exact_tour:
                results["exact"] = {
                    "tour": exact_tour,
                    "cost": exact_tour_cost,
                    "time_details": time_details,
                    "totalLoadingTime": exact_tour_cost
                }
                print(f"Exact Method TSP completed. Cost: {exact_tour_cost}")

        except ValueError as e:
            print(f"Error in exact method: {e}")

    #Select the method with the minimum cost if "all" was specified
    if method == "all":
        min_cost_method = min(results, key=lambda k: results[k]["cost"])
        results = {min_cost_method: results[min_cost_method]}
        print(f"Selected method with minimum cost: {min_cost_method}")

    end_time = int(time() * 1000)

    picking_seq = []

    for method, result in results.items():
        if "time_details" in result:
            picking_seq.append({
                "method": method
            })
            picking_seq.extend(result["time_details"])
            total_loading_time = result["totalLoadingTime"]

    print("Picking Sequence:")
    for pick in picking_seq:
        print(pick)

    output_data_local = {
        "uuid": input_data['uuid'],
        "produced_at": int(time() * 1000),
        "data": {
            "pickingSeq": picking_seq,
            "totalLoadingTime": str(total_loading_time),
            "solutionTime": (end_time - solution_time_start),
            "totalTime": (end_time - total_time_start)
        }
    }
    print(output_data_local)
    #convert all data to native Python types
    output_data_local = convert_to_native_types(output_data_local)

    with open(output_json_file_path, 'w') as json_file:
        json.dump(output_data_local, json_file, indent=4)

    print(f"Output JSON has been saved to {output_json_file_path}")
    return output_data_local

def convert_to_native_types_reverse(data):
    if isinstance(data, dict):
        return {key: convert_to_native_types_reverse(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_to_native_types_reverse(element) for element in data]
    elif isinstance(data, (int, float, str)):
        return data
    else:
        return str(data)

def process_json_data(input_data):
    #save the JSON input to a file
    total_time_start = int(time() * 1000)
    a_to_b_matrix, b_to_a_matrix = create_distance_matrices_from_postman(input_data)
    print(a_to_b_matrix)
    print(b_to_a_matrix)
    print("Distance matrices created!")

    #Create the bipartite graph
    B, set_1, set_2 = create_bipartite_graph(a_to_b_matrix, b_to_a_matrix)
    print("Graph generated!")

    start_node = input_data['data'].get('start_node', '0.0.0')
    end_node = input_data['data'].get('end_node', '0.0.0')
    method = input_data['data']['method']

    #adding the start/end node to the set_2 list explicitly
    if end_node not in set_2:
        set_2.append(end_node)

    results = {}
    solution_time_start = int(time() * 1000)
    simple_tour = None

    if method == "nearest" or method == "all":
        try:
            print("Running Nearest Neighbor TSP...")
            simple_tour = nearest_tsp(B, start_node, end_node, set_1, set_2)
            simple_tour_cost, time_details = total_cost(B, simple_tour)
            results["nearest"] = {
                "tour": simple_tour,
                "cost": simple_tour_cost,
                "time_details": time_details,
                "totalLoadingTime": simple_tour_cost
            }
            print(f"Nearest Neighbor TSP. Cost: {simple_tour_cost}")
        except ValueError as e:
            print(f"Error in nearest method: {e}")
            output_data = {
                "uuid": input_data['uuid'],
                "generated_at": int(time() * 1000),
                "data": {
                    "Message": str(e)
                }
            }
            return output_data

    # 2-opt Optimization
    if method == "2-opt" or method == "all":
        try:
            print("Running 2-opt optimization...")
            # if nearest_tsp was not run before, generate the tour first
            if simple_tour is None:
                print("Nearest neighbor tour not found, generating it for 2-opt...")
                simple_tour = nearest_tsp(B, start_node, end_node, set_1, set_2)

            optimized_tour = opt2(simple_tour, B, set_1, set_2, start_node, end_node)
            optimized_tour_cost, time_details = total_cost(B, optimized_tour)
            results["2-opt"] = {
                "tour": optimized_tour,
                "cost": optimized_tour_cost,
                "time_details": time_details,
                "totalLoadingTime": optimized_tour_cost
            }
            print(f"2-opt TSP completed. Cost: {optimized_tour_cost}")
        except ValueError as e:
            print(f"Error in 2-opt method: {e}")
            output_data = {
                "uuid": input_data['uuid'],
                "generated_at": int(time() * 1000),
                "data": {
                    "Message": str(e)
                }
            }
            return output_data

    if method == "q-learning" or method == "all":
        try:
            print("Running Q-Learning TSP...")
            q_learning_tour = q_learning_tsp(B, start_node, end_node, set_1, set_2)
            q_learning_tour_cost, time_details = total_cost(B, q_learning_tour)
            results["q-learning"] = {
                "tour": q_learning_tour,
                "cost": q_learning_tour_cost,
                "time_details": time_details,
                "totalLoadingTime": q_learning_tour_cost
            }
            print(f"Q-Learning TSP completed. Cost: {q_learning_tour_cost}")
        except ValueError as e:
            print(f"Error in q-learning method: {e}")
            output_data = {
                "uuid": input_data['uuid'],
                "generated_at": int(time() * 1000),
                "data": {
                    "Message": str(e)
                }
            }
            return output_data

    # Exact Method TSP
    if method == "exact" or method == "all":
        try:
            print("Running Exact Method TSP...")

            # Call the exact TSP function from old_exact_method.py
            exact_tour, exact_tour_cost, time_details = run_exact_tsp_remote(input_data)

            if exact_tour:
                results["exact"] = {
                    "tour": exact_tour,
                    "cost": exact_tour_cost,
                    "time_details": time_details,
                    "totalLoadingTime": exact_tour_cost
                }
                print(f"Exact Method TSP completed. Cost: {exact_tour_cost}")
        except ValueError as e:
            print(f"Error in exact method: {e}")
            output_data = {
                "uuid": input_data['uuid'],
                "generated_at": int(time() * 1000),
                "data": {
                    "Message": str(e)
                }
            }
            return output_data

    #Select the method with the minimum cost if "all" was specified
    if method == "all":
        min_cost_method = min(results, key=lambda k: results[k]["cost"])
        results = {min_cost_method: results[min_cost_method]}
        print(f"Selected method with minimum cost: {min_cost_method}")

    end_time = int(time() * 1000)
    picking_seq = []
    for method, result in results.items():
        if "time_details" in result:
            picking_seq.append({
                "method": method
            })
            picking_seq.extend(result["time_details"])
            total_loading_time = result["totalLoadingTime"]
    print("Picking Sequence:")
    for pick in picking_seq:
        print(pick)

    output_data = {
        "uuid": input_data['uuid'],
        "produced_at": int(time() * 1000),
        "data": {
            "pickingSeq": picking_seq,
            "totalLoadingTime": str(total_loading_time),
            "solutionTime": (end_time - solution_time_start),
            "totalTime": (end_time - total_time_start)
        }
    }
    # reverse all data from native Python types to JSON types
    output_data = convert_to_native_types_reverse(output_data)
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
        output = process_json_data(input_file)

        print("%s: Publishing results to queue." % (datetime.now().strftime("%d/%m/%Y %H:%M:%S")))

        output = json.dumps(output)
        channel.basic_publish(exchange='opt-result', routing_key='robot-picking-seq', body=output)
        print("%s: Job with uuid: %s completed" % (datetime.now().strftime("%d/%m/%Y %H:%M:%S"), uuid))
    except Exception as e:
        #print(Exception, e)
        print(traceback.format_exc())
        error_message = {"message": str(e)}
        error_responce = {"uuid": uuid, "data": error_message, "produced_at": int(time() * 1000)}
        error_responce = json.dumps(error_responce)
        channel.basic_publish(exchange='opt-result', routing_key='robot-picking-seq', body=error_responce)
        print("%s: Job with uuid: %s failed" % (datetime.now().strftime("%d/%m/%Y %H:%M:%S"), uuid))



if online == "1":
    host = sys.argv[2]
    port = sys.argv[3]
    username = sys.argv[4]
    password = sys.argv[5]
    credentials = pika.PlainCredentials(username, password)
    params = pika.ConnectionParameters(host, port, '/', credentials, heartbeat=1860, blocked_connection_timeout=930)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.basic_consume(queue='robot-picking-seq_job',
                          auto_ack=True,
                          on_message_callback=callback)
    channel.start_consuming()
if online == "0":
    filename = sys.argv[2]
    with open(filename) as f:
        input = json.load(f)
    print(datetime.now(), " - Data Received Successfully.")
    uuid = input['uuid']
    print(f"Process UUID: {input['uuid']}")
    # print(input['data'])
    input_data = input['data']

    json_file_path = "random_json_input.json"
    output_json_file_path = "output_tsp_results.json"

    #run the TSP algorithm for the JSON input
    run_tsp_for_size(json_file_path, output_json_file_path)