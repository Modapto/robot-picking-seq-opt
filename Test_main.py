import json
import traceback
from datetime import datetime
from time import time
import pandas as pd
import numpy as np
import os
from parse_json import *
from GraphCreation import *
from heuristic_methods import *
from reinforcement_learning import *
from exact_method import *
from Test_instances_generator import *

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

def run_tsp(json_file_path, output_json_file_path, gravity_rack_positions=None, kit_holder_positions=None):
    total_time_start = int(time() * 1000)
    total_loading_time = None  # Initialize here to avoid UnboundLocalError

    # # Step 1: Generate a new random JSON instance if generate_new_instance is True
    # if generate_new_instance:
    #     random_json_input = generate_random_json_input()  # Assuming this function creates a valid JSON structure
    #     json_file_path = "random_json_input.json"  # Path to save the new random JSON file
    #     with open(json_file_path, 'w') as json_file:
    #         json.dump(random_json_input, json_file, indent=4)
    #     print(f"New random JSON input has been generated and saved to {json_file_path}.")
    #
    #     # Load this new input for further processing
    #     input_data = random_json_input
    # else:
    #     # Load input from file if it's not set to generate a new instance
    #     if json_file_path:
    #         with open(json_file_path, 'r') as f:
    #             input_data = json.load(f)
    #         print(f"Local JSON input has been loaded from {json_file_path}.")
    #     elif input_data:
    #         print("Remote input data received.")
    #     else:
    #         raise ValueError("Input data is required, either via JSON file or directly.")

    # Load the input data
    with open(json_file_path, 'r') as json_file:
        input_data = json.load(json_file)

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

    try:
        print("Running Nearest Neighbor TSP...")
        start_time_nearest = (time() * 1000)
        simple_tour = nearest_tsp(B, start_node, end_node, set_1, set_2)
        simple_tour_cost, time_details = total_cost(B, simple_tour)
        exec_time_nearest = (time() * 1000) - start_time_nearest
        results["nearest"] = {
            "tour": simple_tour,
            "cost": simple_tour_cost,
            "exec_time": exec_time_nearest,
            "time_details": time_details
        }
        print(f"Nearest Neighbor TSP. Cost: {simple_tour_cost}")
    except ValueError as e:
        print(f"Error in nearest method: {e}")

    try:
        print("Running 2-Opt Optimization...")
        start_time_2opt = (time() * 1000)
        optimized_tour = opt2(simple_tour, B, set_1, set_2, start_node, end_node)
        optimized_tour_cost, time_details = total_cost(B, optimized_tour)
        exec_time_2opt = (time() * 1000) - start_time_2opt
        results["2-opt"] = {
            "tour": optimized_tour,
            "cost": optimized_tour_cost,
            "exec_time": exec_time_2opt,
            "time_details": time_details
        }
        print("2-Opt Optimization completed.")
    except ValueError as e:
        print(f"Error in 2-opt method: {e}")

    try:
        print("Running Q-Learning TSP...")
        start_time_qlearning = (time() * 1000)
        q_learning_tour = q_learning_tsp(B, start_node, end_node, set_1, set_2)
        q_learning_tour_cost, time_details = total_cost(B, q_learning_tour)
        exec_time_qlearning = (time() * 1000) - start_time_qlearning
        results["q-learning"] = {
            "tour": q_learning_tour,
            "cost": q_learning_tour_cost,
            "exec_time": exec_time_qlearning,
            "time_details": time_details
        }
        print(f"Q-Learning TSP completed. Cost: {q_learning_tour_cost}")
    except ValueError as e:
        print(f"Error in q-learning method: {e}")


    try:
        print("Running Exact Method TSP...")
        start_time_exact = (time() * 1000)
        exact_tour, exact_tour_cost, time_details = run_exact_tsp(input_data)
        exec_time_exact = (time() * 1000) - start_time_exact
        if exact_tour:
            results["exact"] = {
                "tour": exact_tour,
                "cost": exact_tour_cost,
                "exec_time": exec_time_exact,
                "time_details": time_details
            }
            print(f"Exact Method TSP completed. Cost: {exact_tour_cost}")
    except ValueError as e:
        print(f"Error in exact method: {e}")

    #Convert all data to native Python types to avoid JSON serialization issues
    results = convert_to_native_types(results)

    #ave the results to a file
    with open(output_json_file_path, 'w') as json_file:
        json.dump(results, json_file, indent=4)

    return results


def save_results_to_csv(results, gravity_rack, kit_holder, run_id):
    df_results = pd.DataFrame(results)
    filename = f"experiment_results/GR_{gravity_rack}_KH_{kit_holder}_Run_{run_id}.csv"
    os.makedirs("experiment_results", exist_ok=True)
    df_results.to_csv(filename, index=False)
    print(f"Results saved to {filename}")
