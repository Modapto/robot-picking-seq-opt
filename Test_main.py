import json
import traceback
from datetime import datetime
from time import time
import pandas as pd
import numpy as np
import os
from parse_json_input import *
from GraphCreation import *
from Solver import *
from exact_method import *
from Test_generate_random_input import *


def convert_to_native_types(data):
    if isinstance(data, dict):
        return {k: convert_to_native_types(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_to_native_types(v) for v in data]
    elif isinstance(data, np.integer):
        return int(data)
    elif isinstance(data, (np.float32, np.float64)):
        return float(data)
    else:
        return data

def run_tsp_for_size(json_file_path, output_json_file_path, gravity_rack_positions=None, kit_holder_positions=None):
    #Load the JSON input from the provided file
    with open(json_file_path, 'r') as json_file:
        random_json_input = json.load(json_file)

    results = {}

    a_to_b_matrix, b_to_a_matrix = create_distance_matrices_from_json(json_file_path)
    B, set_1, set_2 = create_bipartite_graph(a_to_b_matrix, b_to_a_matrix)
    start_node = random_json_input['data']['start_node']
    end_node = random_json_input['data']['end_node']
    simple_tour = 0
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
        print("Nearest Neighbor TSP completed.")
    except ValueError as e:
        print(f"Error in nearest method: {e}")

    try:
        print("Running 2-Opt Optimization...")
        start_time_2opt = (time() * 1000)
        optimized_tour = opt2(simple_tour, B, set_1, set_2, start_node, end_node)  # Run 2-opt after Nearest
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
        exact_tour, exact_tour_cost, time_details = run_exact_tsp_local(json_file_path)  # Use the exact method
        exec_time_exact = (time() * 1000) - start_time_exact
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
