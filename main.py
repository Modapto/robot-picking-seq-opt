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
# from parametric_instances import *
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

def run_tsp(json_file_path, input_data, generate_new_instance):
    """
    Main function to run the TSP solution process.

    Parameters:
    - json_file_path: Path to the JSON input file (if applicable).
    - input_data: JSON data directly provided (e.g., for remote runs).
    - generate_new_instance: Flag to generate a random JSON instance.

    Returns:
    - output_data: Results of the TSP solution.
    """
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
    improvement = 0
    # Run methods based on the input's method
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
                optimized_tour, optimized_tour_cost = two_opt_for_bipartite(simple_tour, B, set_1, set_2, max_iterations=1000)
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
                    print(f"2-opt TSP. Cost: {best_cost}")
                results["2-opt"] = {
                    "tour": best_tour,
                    "cost": best_cost,
                    "time_details": time_details,
                    "totalLoadingTime": best_cost
                }
            except ValueError as e:
                print(f"Error in 2-opt method: {e}")

    if method == "q-learning" or method == "all":
        try:
            print("Running Q-Learning TSP...")
            q_learning_tour = q_learning_tsp(B, start_node, end_node, set_1, set_2)
            q_learning_tour_cost, time_details = total_costRL(B, q_learning_tour)
            results["q-learning"] = {
                "tour": q_learning_tour,
                "cost": q_learning_tour_cost,
                "time_details": time_details,
                "totalLoadingTime": q_learning_tour_cost
            }
            print(f"Q-Learning TSP completed. Cost: {q_learning_tour_cost}")
        except ValueError as e:
            print(f"Error in q-learning method: {e}")

    if method == "ql-nearest" or method == "all":
        try:
            print("Running Q-Learning Nearest Neighbor TSP...")
            ql_simple_tour = ql_nearest_tsp(B, start_node, end_node, set_1, set_2)
            ql_simple_tour_cost, ql_time_details = total_cost(B, ql_simple_tour)
            results["ql-nearest"] = {
                "tour": ql_simple_tour,
                "cost": ql_simple_tour_cost,
                "time_details": ql_time_details,
                "totalLoadingTime": ql_simple_tour_cost
            }
            print(f"Q-Learning Nearest Neighbor TSP. Cost: {ql_simple_tour_cost}")
        except ValueError as e:
            print(f"Error in QL-Nearest method: {e}")

    ql_simple_tour = None  # Initialize to avoid UnboundLocalError
    if method == "ql-2-opt" or method == "all":
            try:
                if ql_simple_tour is None:
                    print("No Q-Learning tour found. Generating initial tour using QL-Nearest Neighbor...")
                    ql_simple_tour = ql_nearest_tsp(B, start_node, end_node, set_1, set_2)
                    ql_simple_tour_cost, ql_time_details = total_cost(B, ql_simple_tour)
                    print(f"QL-Nearest TSP generated with cost: {ql_simple_tour_cost}")

                print("Running Q-Learning 2-opt TSP...")
                ql_optimized_tour, ql_optimized_tour_cost = ql_two_opt_for_bipartite(
                    ql_simple_tour, B, set_1, set_2, max_iterations=1000
                )
                ql_optimized_tour_cost, ql_time_details = total_cost(B, ql_optimized_tour)

                # Compare costs and choose the better solution
                if ql_optimized_tour_cost < ql_simple_tour_cost:
                    print(
                        f"2-opt improved the tour. Cost reduced from {ql_simple_tour_cost} to {ql_optimized_tour_cost}")
                    ql_best_tour = ql_optimized_tour
                    ql_best_cost = ql_optimized_tour_cost
                else:
                    print(f"2-opt did not improve the tour. Keeping the Q-Learning Nearest Neighbor solution.")
                    ql_best_tour = ql_simple_tour
                    ql_best_cost = ql_simple_tour_cost

                results["ql-2-opt"] = {
                    "tour": ql_best_tour,
                    "cost": ql_best_cost,
                    "time_details": ql_time_details,
                    "totalLoadingTime": ql_best_cost
                }
                print(f"Q-Learning 2-opt TSP. Cost: {ql_best_cost}")
            except ValueError as e:
                print(f"Error in QL-2-opt method: {e}")

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

    if method == "linear" or method == "all":
        try:
            print("Running Linear Method TSP...")
            linear_tour = linear_picking(B, start_node, end_node, set_1, set_2)
            linear_tour_cost, time_details = total_cost(B, linear_tour['tour'])

            if linear_tour:
                results["linear"] = {
                    "tour": linear_tour,
                    "cost": linear_tour_cost,
                    "time_details": time_details,
                    "totalLoadingTime": linear_tour_cost
                }
                print(f"Linear Method TSP completed. Cost: {linear_tour_cost}")
        except ValueError as e:
            print(f"Error in exact method: {e}")

    if method == "exact-linear" or method == "all":
        try:
            print("Running Exact + Linear Method TSP...")
            exact_tour, exact_tour_cost, time_details_exact = run_exact_tsp(input_data)
            linear_tour = linear_picking(B, start_node, end_node, set_1, set_2)
            linear_tour_cost, time_details_linear = total_cost(B, linear_tour['tour'])
            improvement = ((linear_tour_cost - exact_tour_cost) / linear_tour_cost) * 100

            if improvement > 0:
                results["exact"] = {
                    "tour": exact_tour,
                    "cost": exact_tour_cost,
                    "time_details": time_details_exact,
                    "totalLoadingTime": exact_tour_cost
                }
                print(f"Exact Method TSP is better. Cost: {exact_tour_cost}")
            else:
                results["linear"] = {
                    "tour": linear_tour,
                    "cost": linear_tour_cost,
                    "time_details": time_details_linear,
                    "totalLoadingTime": linear_tour_cost
                }
                print(f"Linear Method TSP is better. Cost: {linear_tour_cost}")

        except ValueError as e:
            print(f"Error in exact method: {e}")

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
            "totalTime": (end_time - total_time_start),
            "improvement": improvement
        }
    }

    output_data = convert_to_native_types(output_data)

    if json_file_path:
        output_json_file_path = "output_tsp_results.json"
        with open(output_json_file_path, 'w') as json_file:
            json.dump(output_data, json_file, indent=4)
        print(f"Local output saved to {output_json_file_path}")

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
        error_message = {"message": str(e)}
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

    if input_data["data"].get("method") == "simulation":
        print("Running simulation...")
        run_simulation(input_data)
    else:
        print("Running optimization...")
        run_tsp(json_file_path=filename, input_data=None, generate_new_instance=False)
