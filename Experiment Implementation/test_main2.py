import json
from time import time
import pandas as pd
import numpy as np
import os
from GraphCreation import create_distance_matrices, create_directed_bipartite_graph
from heuristic_methods import nearest_tsp, two_opt_for_bipartite, total_cost
from reinforcement_learning import q_learning_tsp
from exact_method import run_exact_tsp
from rl_heuristics import *
from method_linear import *


def convert_to_native_types(data):
    if isinstance(data, dict):
        return {k: convert_to_native_types(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_to_native_types(v) for v in data]
    elif isinstance(data, pd.DataFrame):
        return data.applymap(lambda x: int(x) if isinstance(x, (np.integer, np.int32, np.int64)) else x).to_dict()
    elif isinstance(data, (np.integer, np.int32, np.int64)):
        return int(data)
    elif isinstance(data, (np.floating, np.float32, np.float64)):
        return float(data)
    elif isinstance(data, np.ndarray):  # If there are any numpy arrays, convert them to lists
        return data.tolist()
    else:
        return data


# def is_feasible(input_json):
#     try:
#         # Parse distance matrices and create the graph
#         a_to_b_matrix = create_distance_matrices(input_json)
#         B, set_1, set_2 = create_directed_bipartite_graph(a_to_b_matrix)
#
#         # Retrieve start and end nodes
#         start_node = input_json['data'].get('start_node', '0.0')
#         end_node = input_json['data'].get('end_node', '0.0.0')
#
#         # Run the nearest neighbor function to test feasibility
#         nearest_tour = nearest_tsp(B, start_node, end_node, set_1, set_2)
#         return True  # If it completes without error, the instance is feasible
#     except ValueError as e:
#         print(f"Infeasible instance detected in nearest neighbor check: {e}")
#         return False


def run_tsp(json_file_path, output_json_file_path, gravity_rack_positions=None, kit_holder_positions=None):
    with open(json_file_path, 'r') as json_file:
        input_data = json.load(json_file)

    # Parse the distance matrices
    a_to_b_matrix = create_distance_matrices(input_data)
    print("Distance matrices created!")

    # Create the bipartite graph
    B, set_1, set_2 = create_directed_bipartite_graph(a_to_b_matrix)
    print("Graph generated!")

    start_node = input_data['data'].get('start_node', '0.0')
    end_node = input_data['data'].get('end_node', '0.0.0')

    results = {}

    # # Run Nearest Neighbor TSP
    # try:
    #     print("Running Nearest Neighbor TSP...")
    #     start_time_nearest = time() * 1000
    #     simple_tour = nearest_tsp(B, start_node, end_node, set_1, set_2)
    #     simple_tour_cost, time_details = total_cost(B, simple_tour)
    #     exec_time_nearest = (time() * 1000) - start_time_nearest
    #     results["nearest"] = {
    #         "tour": simple_tour,
    #         "cost": simple_tour_cost,
    #         "exec_time": exec_time_nearest,
    #         "time_details": time_details
    #     }
    #     print(f"Nearest Neighbor TSP completed. Cost: {simple_tour_cost}")
    # except ValueError as e:
    #     print(f"Error in nearest method: {e}")
    try:
        print("Running Linear Method TSP...")
        start_time_linear = time() * 1000
        linear_tour = linear_picking(B, start_node, end_node, set_1, set_2)
        linear_tour_cost, time_details = total_cost(B, linear_tour['tour'])
        exec_time_linear = (time() * 1000) - start_time_linear
        results["linear"] = {
            "tour": linear_tour,
            "cost": linear_tour_cost,
            "exec_time": exec_time_linear,
            "time_details": time_details
        }
        print(f"Linear Method TSP completed. Cost: {linear_tour_cost}")
    except ValueError as e:
        print(f"Error in linear method: {e}")
    # # Run 2-Opt Optimization
    # try:
    #     print("Running 2-Opt Optimization...")
    #     start_time_2opt = time() * 1000  # Initialize start time for 2-opt
    #
    #     # If there's no initial tour, generate one using Nearest Neighbor
    #     if not simple_tour:
    #         print("No initial tour found. Generating one with Nearest Neighbor for 2-opt.")
    #         simple_tour = nearest_tsp(B, start_node, end_node, set_1, set_2)
    #         simple_tour_cost, _ = total_cost(B, simple_tour)
    #         print(f"Nearest Neighbor Initial Tour Cost: {simple_tour_cost}")
    #
    #     # Run the 2-opt optimization function
    #     optimized_tour, optimized_tour_cost = two_opt_for_bipartite(simple_tour, B, set_1, set_2, max_iterations=1000)
    #
    #     # Calculate total cost for the optimized tour
    #     final_optimized_cost, time_details = total_cost(B, optimized_tour)
    #
    #     # Compare and choose the best solution
    #     if final_optimized_cost < simple_tour_cost:
    #         print(f"2-opt improved the tour. Cost reduced from {simple_tour_cost} to {final_optimized_cost}")
    #         best_tour = optimized_tour
    #         best_cost = final_optimized_cost
    #     else:
    #         print("2-opt did not improve the tour. Keeping the Nearest Neighbor solution.")
    #         best_tour = simple_tour
    #         best_cost = simple_tour_cost
    #
    #     # Store the results
    #     exec_time_2opt = (time() * 1000) - start_time_2opt
    #     results["2-opt"] = {
    #         "tour": best_tour,
    #         "cost": best_cost,
    #         "exec_time": exec_time_2opt,
    #         "time_details": time_details
    #     }
    #     print(f"2-opt TSP completed. Final Cost: {best_cost}")
    #
    # except ValueError as e:
    #     print(f"Error in 2-opt method: {e}")
    #     results["2-opt"] = {
    #         "tour": [],
    #         "cost": None,
    #         "exec_time": None,
    #         "time_details": f"Error: {e}"
    #     }
    # except Exception as e:
    #     print(f"Unexpected error in 2-opt method: {e}")
    #     results["2-opt"] = {
    #         "tour": [],
    #         "cost": None,
    #         "exec_time": None,
    #         "time_details": f"Unexpected error: {e}"
    #     }
    #
    # # Run Q-Learning TSP
    # try:
    #     print("Running Q-Learning TSP...")
    #     start_time_qlearning = time() * 1000
    #     q_learning_tour = q_learning_tsp(B, start_node, end_node, set_1, set_2)
    #     q_learning_tour_cost, time_details = total_cost(B, q_learning_tour)
    #     exec_time_qlearning = (time() * 1000) - start_time_qlearning
    #     results["q-learning"] = {
    #         "tour": q_learning_tour,
    #         "cost": q_learning_tour_cost,
    #         "exec_time": exec_time_qlearning,
    #         "time_details": time_details
    #     }
    #     print(f"Q-Learning TSP completed. Cost: {q_learning_tour_cost}")
    # except ValueError as e:
    #     print(f"Error in q-learning method: {e}")
    #
    # try:
    #     print("Running Q-Learning Nearest Neighbor TSP...")
    #     start_time_ql_nearest = time() * 1000
    #     qlnn_simple_tour = ql_nearest_tsp(B, start_node, end_node, set_1, set_2)
    #     qlnn_simple_tour_cost, qlnn_time_details = total_cost(B, qlnn_simple_tour)
    #     exec_time_ql_nearest = (time() * 1000) - start_time_ql_nearest
    #     results["ql-nearest"] = {
    #         "tour": qlnn_simple_tour,
    #         "cost": qlnn_simple_tour_cost,
    #         "exec_time": exec_time_ql_nearest,
    #         "time_details": time_details
    #     }
    #     print(f"Q-Learning Nearest Neighbor TSP. Cost: {qlnn_simple_tour_cost}")
    # except ValueError as e:
    #     print(f"Error in QL-Nearest method: {e}")
    #
    # qlnn_simple_tour = None  # Initialize to avoid UnboundLocalError
    # try:
    #     print("Running 2-Opt Optimization...")
    #     start_time_ql_2opt = time() * 1000  # Initialize start time for 2-opt
    #
    #     # If there's no initial tour, generate one using Nearest Neighbor
    #     if not qlnn_simple_tour:
    #         print("No initial tour found. Generating one with Nearest Neighbor for 2-opt.")
    #         qlnn_simple_tour = ql_nearest_tsp(B, start_node, end_node, set_1, set_2)
    #         qlnn_simple_tour_cost, _ = total_cost(B, qlnn_simple_tour)
    #         print(f"Nearest Neighbor Initial Tour Cost: {qlnn_simple_tour_cost}")
    #
    #     ql2opt_optimized_tour, ql2opt_optimized_tour_cost = ql_two_opt_for_bipartite(
    #         qlnn_simple_tour, B, set_1, set_2, max_iterations=1000
    #     )
    #     ql2opt_optimized_tour_cost, ql2opt_time_details = total_cost(B, ql2opt_optimized_tour)
    #
    #     # Compare costs and choose the better solution
    #     if ql2opt_optimized_tour_cost < qlnn_simple_tour_cost:
    #         print(
    #             f"2-opt improved the tour. Cost reduced from {ql2opt_simple_tour_cost} to {ql2opt_optimized_tour_cost}")
    #         ql2opt_best_tour = ql2opt_optimized_tour
    #         ql2opt_best_cost = ql2opt_optimized_tour_cost
    #     else:
    #         print(f"2-opt did not improve the tour. Keeping the Q-Learning Nearest Neighbor solution.")
    #         ql2opt_best_tour = qlnn_simple_tour
    #         ql2opt_best_cost = qlnn_simple_tour_cost
    #     exec_time_ql_2opt = (time() * 1000) - start_time_ql_2opt
    #     results["ql-2-opt"] = {
    #         "tour": ql2opt_best_tour,
    #         "cost": ql2opt_best_cost,
    #         "exec_time": exec_time_ql_2opt,
    #         "time_details": time_details
    #     }
    #     print(f"Q-Learning 2-opt TSP. Cost: {ql2opt_best_cost}")
    # except ValueError as e:
    #     print(f"QL-2-opt failed: {e}")
    #     results["ql-2-opt"] = {
    #         "tour": None,
    #         "cost": None,
    #         "exec_time": None,
    #         "time_details": f"Error: {e}"
    #     }
    # Run Exact Method TSP
    try:
        print("Running Exact Method TSP...")
        start_time_exact = time() * 1000
        exact_tour, exact_tour_cost, time_details = run_exact_tsp(input_data)
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

    # Convert all data to native Python types for JSON serialization
    results = convert_to_native_types(results)

    # Save the results to a file
    with open(output_json_file_path, 'w') as json_file:
        json.dump(results, json_file, indent=4)

    return results


def save_results_to_csv(results, gravity_rack, kit_holder, run_id):
    # Convert results to DataFrame for easy CSV export
    data = []
    for method, res in results.items():
        data.append({
            "Method": method,
            "Tour": res["tour"],
            "Cost": res["cost"],
            "Execution Time (ms)": res["exec_time"],
            "Time Details": res["time_details"]
        })

    df_results = pd.DataFrame(data)
    filename = f"experiment_results/GR_{gravity_rack}_KH_{kit_holder}_Run_{run_id}.csv"
    os.makedirs("experiment_results", exist_ok=True)
    df_results.to_csv(filename, index=False)
    print(f"Results saved to {filename}")
