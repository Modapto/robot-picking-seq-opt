import json
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
from simulator import *
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

# def run_tsp(json_file_path, input_data=None, generate_new_instance=False):
#     total_time_start = int(time() * 1000)
#
#     # Load input data
#     if input_data and "data" in input_data:
#         print("Remote input data received.")
#         data = input_data["data"]
#         distance_matrix = data["distance_matrix"]
#         containers_template = data["containers_template"]
#         kit_holders_template = data["kit_holders_template"]
#         kh_setup = data["kh_setup"]
#         current_config = data["current_config"]
#     elif json_file_path:
#         with open(json_file_path, 'r') as f:
#             input_data = json.load(f)
#         data = input_data["data"]
#         distance_matrix = data["distance_matrix"]
#         containers_template = data["containers_template"]
#         kit_holders_template = data["kit_holders_template"]
#         kh_setup = data["kh_setup"]
#         current_config = data["current_config"]
#         print(f"Local JSON input has been loaded from {json_file_path}.")
#     else:
#         raise ValueError("Input data is required, either via JSON file or directly.")
#
#     # Generate KH configuration
#     kh_config = generate_kh_configuration(kh_setup, kit_holders_template)
#
#     # Generate filtered distance matrix based on current configuration
#     filtered_matrix = filter_distance_matrix(distance_matrix, {
#         "containers": current_config["containers"],
#         "kit_holders": kh_config
#     })
#
#     # Parse the filtered distance matrix
#     a_to_b_matrix = create_distance_matrices({
#         "data": {
#             "distanceMatrix": filtered_matrix
#         }
#     })
#     print(a_to_b_matrix)
#     # Create the bipartite graph
#     B, set_1, set_2 = create_directed_bipartite_graph(a_to_b_matrix)
#     start_node = data.get('start_node', '0.0')
#     end_node = data.get('end_node', '0.0.0')
#     method = data['method']
#     print(set_1, set_2)
#     results = {}
#     solution_time_start = int(time() * 1000)
#     simple_tour = None
#     improvement = 0
#
#     # Run methods based on the input's method
#     if method == "nearest" or method == "all":
#         try:
#             print("Running Nearest Neighbor TSP...")
#             simple_tour = nearest_tsp(B, start_node, end_node, set_1, set_2)
#             simple_tour_cost, time_details = total_cost(B, simple_tour)
#             results["nearest"] = {
#                 "tour": simple_tour,
#                 "cost": simple_tour_cost,
#                 "time_details": time_details,
#                 "totalLoadingTime": simple_tour_cost
#             }
#             print(f"Nearest Neighbor TSP. Cost: {simple_tour_cost}")
#         except ValueError as e:
#             print(f"Error in nearest method: {e}")
#
#     if method == "2-opt" or method == "all":
#         if simple_tour or method == "2-opt":
#             try:
#                 print("Running 2-opt TSP...")
#                 if not simple_tour and method == "2-opt":
#                     print("No previous tour found. Using Nearest Neighbor to generate initial tour for 2-opt.")
#                     simple_tour = nearest_tsp(B, start_node, end_node, set_1, set_2)
#                     simple_tour_cost, time_details = total_cost(B, simple_tour)
#                     print(f"Nearest Neighbor TSP. Cost: {simple_tour_cost}")
#
#                 # Run 2-opt optimization on the simple tour
#                 optimized_tour, optimized_tour_cost = two_opt_for_bipartite(simple_tour, B, set_1, set_2, max_iterations=1000)
#                 optimized_tour_cost, time_details = total_cost(B, optimized_tour)
#
#                 # Compare costs and choose the better solution
#                 if optimized_tour_cost < simple_tour_cost:
#                     print(f"2-opt improved the tour. Cost reduced from {simple_tour_cost} to {optimized_tour_cost}")
#                     best_tour = optimized_tour
#                     best_cost = optimized_tour_cost
#                 else:
#                     print(f"2-opt did not improve the tour. Keeping the Nearest Neighbor solution.")
#
#                     best_tour = simple_tour
#                     best_cost = simple_tour_cost
#                     print(f"2-opt TSP. Cost: {best_cost}")
#                 results["2-opt"] = {
#                     "tour": best_tour,
#                     "cost": best_cost,
#                     "time_details": time_details,
#                     "totalLoadingTime": best_cost
#                 }
#             except ValueError as e:
#                 print(f"Error in 2-opt method: {e}")
#
#     if method == "q-learning" or method == "all":
#         try:
#             print("Running Q-Learning TSP...")
#             q_learning_tour = q_learning_tsp(B, start_node, end_node, set_1, set_2)
#             q_learning_tour_cost, time_details = total_costRL(B, q_learning_tour)
#             results["q-learning"] = {
#                 "tour": q_learning_tour,
#                 "cost": q_learning_tour_cost,
#                 "time_details": time_details,
#                 "totalLoadingTime": q_learning_tour_cost
#             }
#             print(f"Q-Learning TSP completed. Cost: {q_learning_tour_cost}")
#         except ValueError as e:
#             print(f"Error in q-learning method: {e}")
#
#     if method == "exact" or method == "all":
#         try:
#             print("Running Exact Method TSP...")
#             # Use the filtered matrix for the exact method
#             exact_input = {
#                 "data": {
#                     "distanceMatrix": filtered_matrix,
#                     "start_node": start_node,
#                     "end_node": end_node
#                 }
#             }
#             exact_tour, exact_tour_cost, time_details = run_exact_tsp(exact_input)
#
#             if exact_tour:
#                 results["exact"] = {
#                     "tour": exact_tour,
#                     "cost": exact_tour_cost,
#                     "time_details": time_details,
#                     "totalLoadingTime": exact_tour_cost
#                 }
#                 print(f"Exact Method TSP completed. Cost: {exact_tour_cost}")
#                 total_loading_time = exact_tour_cost  # Update total loading time
#         except ValueError as e:
#             print(f"Error in exact method: {e}")
#
#     if method == "linear" or method == "all":
#         try:
#             print("Running Linear Method TSP...")
#             linear_tour = linear_picking(B, start_node, end_node, set_1, set_2)
#             linear_tour_cost, time_details = total_cost(B, linear_tour['tour'])
#
#             if linear_tour:
#                 results["linear"] = {
#                     "tour": linear_tour,
#                     "cost": linear_tour_cost,
#                     "time_details": time_details,
#                     "totalLoadingTime": linear_tour_cost
#                 }
#                 print(f"Linear Method TSP completed. Cost: {linear_tour_cost}")
#         except ValueError as e:
#             print(f"Error in exact method: {e}")
#
#     if method == "exact-linear" or method == "all":
#         try:
#             print("Running Exact + Linear Method TSP...")
#             # Use filtered_matrix explicitly for the exact method
#             exact_input = {
#                 "data": {
#                     "distanceMatrix": filtered_matrix,
#                     "start_node": start_node,
#                     "end_node": end_node
#                 }
#             }
#             exact_tour, exact_tour_cost, time_details_exact = run_exact_tsp(exact_input)
#
#             # Run linear picking method
#             linear_tour = linear_picking(B, start_node, end_node, set_1, set_2)
#             linear_tour_cost, time_details_linear = total_cost(B, linear_tour['tour'])
#
#             # Calculate improvement only if exact_tour_cost is valid
#             if exact_tour_cost is not None and linear_tour_cost > 0:
#                 improvement = ((linear_tour_cost - exact_tour_cost) / linear_tour_cost) * 100
#             else:
#                 improvement = None
#
#             # Choose the better method
#             if improvement and improvement > 0:
#                 results["exact"] = {
#                     "tour": exact_tour,
#                     "cost": exact_tour_cost,
#                     "time_details": time_details_exact,
#                     "totalLoadingTime": exact_tour_cost
#                 }
#                 print(f"Exact Method TSP is better. Cost: {exact_tour_cost}")
#             else:
#                 results["linear"] = {
#                     "tour": linear_tour,
#                     "cost": linear_tour_cost,
#                     "time_details": time_details_linear,
#                     "totalLoadingTime": linear_tour_cost
#                 }
#                 print(f"Linear Method TSP is better. Cost: {linear_tour_cost}")
#
#         except ValueError as e:
#             print(f"Error in exact method: {e}")
#
#     if method == "all" and results:
#         min_cost_method = min(results, key=lambda k: results[k]["cost"])
#         results = {min_cost_method: results[min_cost_method]}
#         print(f"Selected method with minimum cost: {min_cost_method}")
#
#     end_time = int(time() * 1000)
#
#     picking_seq = []
#     for method_name, result in results.items():
#         if "time_details" in result:
#             picking_seq.append({"method": method_name})
#             picking_seq.extend(result["time_details"])
#             total_loading_time = result["totalLoadingTime"]
#
#     # Generate output in the OLD format
#     output_data = {
#         "uuid": input_data['uuid'],
#         "produced_at": int(time() * 1000),
#         "data": {
#             "pickingSeq": picking_seq,
#             "totalLoadingTime": total_loading_time,
#             "solutionTime": (end_time - solution_time_start),
#             "totalTime": (end_time - total_time_start),
#             "improvement": round(improvement, 3)
#         }
#     }
#     # convert data to native types before saving
#     output_data = convert_to_native_types(output_data)
#
#     # Save the output to a JSON file
#     output_json_file_path = "output_tsp_results.json"
#     with open(output_json_file_path, 'w') as json_file:
#         json.dump(output_data, json_file, indent=4)
#     print(f"Output saved to {output_json_file_path}")
#
#     return output_data


def run_tsp(json_file_path, input_data=None, generate_new_instance=False):
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

    # Extract data components
    distance_matrix = data["distance_matrix"]
    containers_template = data["containers_template"]
    kit_holders_template = data["kit_holders_template"]
    current_config = data["current_config"]

    # Load KH sequences (new feature)
    kh_sequences = data.get("kh_sequences") or [data.get("kh_setup", [])]

    # Initial start and end nodes
    start_node = data.get('start_node', '0.0')
    end_node = data.get('end_node', '0.0.0')

    results = []
    solution_time_start = int(time() * 1000)
    last_node_visited = start_node  # Track last node of each phase

    for i, kh_setup in enumerate(kh_sequences):
        print(f"\n>>> Running Phase {i+1} with KH Setup: {kh_setup}")

        # Generate KH configuration for the current phase
        kh_config = generate_kh_configuration(kh_setup, kit_holders_template)

        # Generate filtered distance matrix
        filtered_matrix = filter_distance_matrix(distance_matrix, {
            "containers": current_config["containers"],
            "kit_holders": kh_config
        })

        # Rename last visited node as new `0.0` for the current phase
        if i > 0:
            print(f"Renaming {last_node_visited} as the new start node `0.0` in Phase {i+1}")
            for edge in filtered_matrix:
                if edge["edge"].startswith(f"({last_node_visited},"):
                    edge["edge"] = edge["edge"].replace(f"({last_node_visited},", "(0.0,")
                if edge["edge"].endswith(f", {last_node_visited})"):
                    edge["edge"] = edge["edge"].replace(f", {last_node_visited})", ", 0.0)")

        # Parse distance matrix
        a_to_b_matrix = create_distance_matrices({
            "data": {"distanceMatrix": filtered_matrix}
        })

        # Create bipartite graph
        B, set_1, set_2 = create_directed_bipartite_graph(a_to_b_matrix)

        method = data["method"]
        phase_results = {}

        # Run the selected method
        if method == "exact" or method == "all":
            print("Running Exact Method TSP...")
            exact_input = {
                "data": {
                    "distanceMatrix": filtered_matrix,
                    "start_node": "0.0",  # Start from the renamed node
                    "end_node": end_node if i == len(kh_sequences) - 1 else None  # Only use end_node in the last phase
                }
            }
            exact_tour, exact_tour_cost, time_details = run_exact_tsp(exact_input)

            # If this is **not** the last phase, remove last movements to `0.0.0` and `0.0`
            if i < len(kh_sequences) - 1:
                print("Removing last movement to 0.0.0 and 0.0 from tour and cost calculation.")

                # Find the last valid node before 0.0.0
                for j in range(len(exact_tour) - 1, -1, -1):
                    if exact_tour[j][1] == "0.0.0":
                        last_node_visited = exact_tour[j][0]  # Store the last valid node
                        exact_tour = exact_tour[:j]  # Remove the final steps
                        break

                # Filter out unwanted movements from time_details
                filtered_time_details = [
                    step for step in time_details if step["to"] not in ["0.0.0", "0.0"]
                ]

                # Recalculate total cost excluding unnecessary moves
                exact_tour_cost = sum(step["distance"] for step in filtered_time_details)

            else:
                filtered_time_details = time_details  # Keep all steps in the last phase

            phase_results["exact"] = {
                "tour": exact_tour,
                "cost": exact_tour_cost,  # Updated cost without 0.0.0 movements
                "time_details": filtered_time_details  # Updated time details
            }

            last_node_visited = exact_tour[-1][1] if exact_tour else last_node_visited  # Update last visited node

        results.append(phase_results)

    end_time = int(time() * 1000)

    # Final Output Data
    output_data = {
        "uuid": input_data['uuid'],
        "produced_at": int(time() * 1000),
        "data": {
            "phases": results,
            "solutionTime": (end_time - solution_time_start),
            "totalTime": (end_time - total_time_start),
        }
    }
    output_data = convert_to_native_types(output_data)
    # Save output to JSON file
    output_json_file_path = "output_tsp_results.json"
    with open(output_json_file_path, 'w') as json_file:
        json.dump(output_data, json_file, indent=4)

    print(f"Output saved to {output_json_file_path}")
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
