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
    total_loading_time = None  # Initialize here to avoid UnboundLocalError

    # Step 1: Generate a new random JSON instance if generate_new_instance is True
    if generate_new_instance:
        random_json_input = generate_random_json_input()  # Assuming this function creates a valid JSON structure
        json_file_path = "random_json_input.json"  # Path to save the new random JSON file
        with open(json_file_path, 'w') as json_file:
            json.dump(random_json_input, json_file, indent=4)
        print(f"New random JSON input has been generated and saved to {json_file_path}.")

        # Load this new input for further processing
        input_data = random_json_input
    else:
        # Load input from file if it's not set to generate a new instance
        if json_file_path:
            with open(json_file_path, 'r') as f:
                input_data = json.load(f)
            print(f"Local JSON input has been loaded from {json_file_path}.")
        elif input_data:
            print("Remote input data received.")
        else:
            raise ValueError("Input data is required, either via JSON file or directly.")

    # Parse the distance matrices
    a_to_b_matrix = create_distance_matrices(input_data)
    print(a_to_b_matrix)
    print("Distance matrices created!")

    # Create the bipartite graph
    B, set_1, set_2 = create_directed_bipartite_graph(a_to_b_matrix)
    print("Graph generated!")

    start_node = input_data['data'].get('start_node', '0.0')
    end_node = input_data['data'].get('end_node', '0.0.0')
    method = input_data['data']['method']

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

    if method == "2-opt" or method == "all":
        if simple_tour or method == "2-opt":
            try:
                print("Running 2-opt TSP...")
                if not simple_tour and method == "2-opt":
                    print("No previous tour found. Using Nearest Neighbor to generate initial tour for 2-opt.")
                    simple_tour = nearest_tsp(B, start_node, end_node, set_1, set_2)
                    simple_tour_cost, time_details = total_cost(B, simple_tour)
                    print(f"Nearest Neighbor TSP. Cost: {simple_tour_cost}")

                # Run 2-opt optimization on the simple tour
                optimized_tour, optimized_tour_cost = two_opt_for_bipartite(simple_tour, B, set_1, set_2, max_iterations=500)
                optimized_tour_cost, time_details = total_cost(B, optimized_tour)

                # Compare costs and choose the better solution
                if optimized_tour_cost < simple_tour_cost:
                    print(f"2-opt improved the tour. Cost reduced from {simple_tour_cost} to {optimized_tour_cost}")
                    best_tour = optimized_tour
                    best_cost = optimized_tour_cost
                else:
                    print(f"2-opt did not improve the tour. Keeping the Nearest Neighbor solution.")
                    best_tour = simple_tour
                    best_cost = simple_tour_cost

                results["2-opt"] = {
                    "tour": best_tour,
                    "cost": best_cost,
                    "time_details": time_details,
                    "totalLoadingTime": best_cost
                }
            except ValueError as e:
                print(f"Error in 2-opt method: {e}")

    if method == "exact" or method == "all":
        try:
            print("Running Exact Method TSP...")
            exact_tour, exact_tour_cost, time_details = run_exact_tsp(input_data)

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

    # Only modifying the Q-learning parts within main.py to handle "nearest-q-learning" and "2opt-q-learning" separately

    # Step 1: Generate Q-values distance matrix if needed for any Q-learning-based method
    q_values_graph = None
    if "nearest-q-learning" in methods or "2opt-q-learning" in methods or "all" in methods:
        try:
            print("Running Q-Learning to generate Q-values matrix...")

            # Run Q-learning to generate Q-values, not a tour
            _, q_df = q_learning_tsp(B, start_node, end_node, set_1, set_2)

            # Create a copy of the original graph and update it with Q-values as weights
            q_values_graph = B.copy()
            for node in q_df.index:
                for neighbor, q_value in q_df.loc[node].items():
                    if q_values_graph.has_edge(node, neighbor):
                        q_values_graph[node][neighbor]['weight'] = q_value
            print("Q-values matrix generated successfully.")

        except ValueError as e:
            print(f"Error in Q-learning training: {e}")

    # Step 2: Run Nearest Neighbor on the Q-values matrix
    if "nearest-q-learning" in methods or "all" in methods:
        try:
            print("Running Nearest Neighbor on Q-values matrix...")
            nn_q_tour = nearest_tsp(q_values_graph, start_node, end_node, set_1, set_2)

            # Calculate the cost of this tour using the original distance matrix
            nn_q_cost_on_real, nn_q_time_details = total_cost(B, nn_q_tour)
            results["nearest-q_learning"] = {
                "tour": nn_q_tour,
                "cost_based_on_real_matrix": nn_q_cost_on_real,
                "time_details": nn_q_time_details,
                "totalLoadingTime": nn_q_cost_on_real
            }
            print(f"Nearest Neighbor on Q-values completed. Cost on original matrix: {nn_q_cost_on_real}")

        except ValueError as e:
            print(f"Error in nearest method on Q-values matrix: {e}")

    # Step 3: Run 2-opt on Q-values matrix
    if "2opt-q-learning" in methods or "all" in methods:
        try:
            print("Running 2-opt optimization on Q-values matrix...")
            # Start 2-opt with an initial tour generated by nearest neighbor on Q-values
            initial_q_tour = nearest_tsp(q_values_graph, start_node, end_node, set_1, set_2)
            optimized_q_tour, _ = two_opt_for_bipartite(initial_q_tour, q_values_graph, set_1, set_2,
                                                        max_iterations=500)

            # Calculate the cost of the optimized tour using the original distance matrix
            optimized_q_cost_on_real, optimized_q_time_details = total_cost(B, optimized_q_tour)
            results["2opt-q_learning"] = {
                "tour": optimized_q_tour,
                "cost_based_on_real_matrix": optimized_q_cost_on_real,
                "time_details": optimized_q_time_details,
                "totalLoadingTime": optimized_q_cost_on_real
            }
            print(f"2-opt on Q-values completed. Cost on original matrix: {optimized_q_cost_on_real}")

        except ValueError as e:
            print(f"Error in 2-opt method on Q-values matrix: {e}")

    if method == "all" and results:
        min_cost_method = min(results, key=lambda k: results[k]["cost"])
        results = {min_cost_method: results[min_cost_method]}
        print(f"Selected method with minimum cost: {min_cost_method}")

    end_time = int(time() * 1000)

    picking_seq = []
    for method, result in results.items():
        if "time_details" in result:
            picking_seq.append({"method": method})
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

    output_data = convert_to_native_types(output_data)

    if json_file_path:
        output_json_file_path = "output_tsp_results.json"
        with open(output_json_file_path, 'w') as json_file:
            json.dump(output_data, json_file, indent=4)
        print(f"Local output saved to {output_json_file_path}")

    return output_data

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