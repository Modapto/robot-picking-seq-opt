import json
import copy
from time import time
import pandas as pd
import numpy as np
from configurations_final import (
    load_distance_matrix,
    load_containers_template,
    load_kit_holders_template,
    randomize_containers,
    filter_distance_matrix
)
from exact_method import run_exact_tsp
from method_linear import *
from GraphCreation import create_directed_bipartite_graph
from parse_json import create_distance_matrices


def generate_unique_gr_configurations(num_configs, containers_template):
    """
    Generate unique random gravity rack configurations.
    """
    configurations = {}
    while len(configurations) < num_configs:
        config = randomize_containers(containers_template)
        key = "-".join(f"{container['gr_position']}:{content['type']}" for container in config.values() for content in
                       container["contents"])
        if key not in configurations:
            configurations[key] = config
    return configurations


def generate_kh_configuration(kh_setup, kit_holders_template):
    """
    Generate kit holder configuration based on the given setup.
    Handles empty positions with the placeholder "EMPTY".
    """
    configured_kh = {}
    for idx, kh_id in enumerate(kh_setup, start=1):
        if kh_id == "EMPTY":
            continue
        if kh_id in kit_holders_template:
            kh_data = copy.deepcopy(kit_holders_template[kh_id])
            for i, content in enumerate(kh_data["contents"], start=1):
                content["position"] = f"{idx}.{i}"
            configured_kh[f"KH{idx}"] = {
                "kh_position": str(idx),
                "contents": kh_data["contents"]
            }
        else:
            raise ValueError(f"Kit holder ID {kh_id} not found.")
    return configured_kh

def calculate_linear_value(distance_matrix, configuration):
    """
    Calculate the objective value for a given configuration using the linear method.
    """
    filtered_matrix = filter_distance_matrix(distance_matrix, configuration)
    a_to_b_matrix = create_distance_matrices({"data": {"distanceMatrix": filtered_matrix}})
    B, set_1, set_2 = create_directed_bipartite_graph(a_to_b_matrix)
    start_node = "0.0"
    end_node = "0.0.0"
    linear_tour = linear_picking(B, start_node, end_node, set_1, set_2)
    tour_cost, _ = total_cost(B, linear_tour["tour"])
    return tour_cost

def calculate_objective_value(distance_matrix, configuration):
    """
    Calculate the objective value of a given configuration using the exact method.
    """
    filtered_matrix = filter_distance_matrix(distance_matrix, configuration)
    tour, cost, _ = run_exact_tsp(
        {"data": {"distanceMatrix": filtered_matrix, "start_node": "0.0", "end_node": "0.0.0"}})
    return cost


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


def run_simulation(input_data=None):
    total_time_start = int(time() * 1000)

    # Load input data
    if input_data and "data" in input_data:
        print("Remote input data received.")
        data = input_data["data"]
        distance_matrix = data["distance_matrix"]
        containers_template = data["containers_template"]
        kit_holders_template = data["kit_holders_template"]
        kh_sequences = data.get("kh_sequences") or [data.get("kh_setup", [])]
        num_random_gr_configs = data["num_random_gr_configs"]
        current_config = data["current_config"]
    else:
        print("Input data not provided, using local files.")
        distance_matrix = load_distance_matrix()
        containers_template = load_containers_template()
        kit_holders_template = load_kit_holders_template()
        kh_sequences = [["KH001", "KH002", "KH001", "KH003"]]
        num_random_gr_configs = 2
        with open("current_config.json", "r") as f:
            current_config = json.load(f)

    # Initial start and end nodes
    start_node = "0.0"
    end_node = "0.0.0"

    baseline_results = []
    simulation_runs = []

    # **Step 1: Calculate Baseline Values for Each KH Sequence**
    last_node_visited = start_node

    for i, kh_setup in enumerate(kh_sequences):
        print(f"\n>>> Running Baseline Phase {i + 1} with KH Setup: {kh_setup}")

        # ✅ Ensure `last_node_visited` is a valid KH ID before inserting it
        if i > 0 and last_node_visited in kit_holders_template:
            print(f"Setting start node to last visited node: {last_node_visited}")
            kh_setup = [last_node_visited] + kh_setup  # Only add if it's a valid KH

        # ✅ Generate KH configuration safely
        try:
            kh_config = generate_kh_configuration(kh_setup, kit_holders_template)
        except ValueError as e:
            print(f"❌ Error in KH Setup {kh_setup}: {e}")
            continue  # Skip invalid setup

        filtered_matrix = filter_distance_matrix(distance_matrix, {
            "containers": current_config["containers"],
            "kit_holders": kh_config
        })

        # **Run Exact Method for Baseline**
        baseline_exact_tour, baseline_exact_cost, _ = run_exact_tsp({
            "data": {
                "distanceMatrix": filtered_matrix,
                "start_node": last_node_visited,
                "end_node": end_node if i == len(kh_sequences) - 1 else None
            }
        })

        # **Update Last Visited Node Only If Valid**
        if i < len(kh_sequences) - 1:
            for j in range(len(baseline_exact_tour) - 1, -1, -1):
                if baseline_exact_tour[j][1] == "0.0.0":
                    last_node_visited = baseline_exact_tour[j][0]
                    break

        baseline_results.append({
            "phase": i + 1,
            "kh_setup": kh_setup,
            "current_value_exact": baseline_exact_cost
        })

    # **Step 2: Simulate Runs with Different GR Configurations**
    gr_configs = generate_unique_gr_configurations(num_random_gr_configs, containers_template)

    for gr_key, gr_config in gr_configs.items():
        print(f"\n>>> Running Simulation with GR Configuration: {gr_key}")
        last_node_visited = start_node
        phase_results = []

        for i, kh_setup in enumerate(kh_sequences):
            print(f"\n>>> Running Simulation Phase {i+1} with KH Setup: {kh_setup}")

            # Ensure last_node_visited is a valid KH before inserting
            if i > 0 and last_node_visited in kit_holders_template:
                print(f"Setting start node to last visited node: {last_node_visited}")
                kh_setup = [last_node_visited] + kh_setup
            else:
                print(f"⚠️ Warning: Last node {last_node_visited} is not a valid KH. Skipping insertion.")

            kh_config = generate_kh_configuration(kh_setup, kit_holders_template)

            filtered_matrix = filter_distance_matrix(distance_matrix, {
                "containers": gr_config,
                "kit_holders": kh_config
            })

            a_to_b_matrix = create_distance_matrices({"data": {"distanceMatrix": filtered_matrix}})
            B, set_1, set_2 = create_directed_bipartite_graph(a_to_b_matrix)

            # **Run Exact Method**
            exact_tour, exact_tour_cost, time_details_exact = run_exact_tsp({
                "data": {
                    "distanceMatrix": filtered_matrix,
                    "start_node": last_node_visited,
                    "end_node": end_node if i == len(kh_sequences) - 1 else None
                }
            })

            # Store last visited node **before** reaching `0.0.0`
            if i < len(kh_sequences) - 1:
                for j in range(len(exact_tour) - 1, -1, -1):
                    if exact_tour[j][1] == "0.0.0":
                        last_node_visited = exact_tour[j][0]
                        break

            phase_results.append({
                "phase": i + 1,
                "kh_setup": kh_setup,
                "objective_value": exact_tour_cost
            })

        # **Store Total Cost for This GR Configuration**
        total_value = sum(p["objective_value"] for p in phase_results)
        simulation_runs.append({
            "gr_config": gr_key,
            "total_value": total_value,
            "sequence_results": phase_results
        })

    # **Step 3: Identify Best GR Configuration**
    best_config = min(simulation_runs, key=lambda x: x["total_value"])

    # **Step 4: Compare Best Simulation Results with Baseline**
    improvement_results = []
    for baseline, phase in zip(baseline_results, best_config["sequence_results"]):
        improvement_exact = round(((baseline["current_value_exact"] - phase["objective_value"]) / baseline["current_value_exact"]) * 100, 3)
        improvement_results.append({
            "phase": baseline["phase"],
            "baseline_value": baseline["current_value_exact"],
            "simulated_value": phase["objective_value"],
            "improvement_exact": improvement_exact
        })

    # **Step 5: Save Final Results**
    end_time = int(time() * 1000)
    output_data = {
        "uuid": input_data['uuid'],
        "produced_at": int(time() * 1000),
        "data": {
            "baseline_results": baseline_results,
            "simulation_runs": simulation_runs,
            "best_total_value": best_config["total_value"],
            "best_configuration": best_config,
            "improvement_results": improvement_results,
            "solutionTime": (end_time - total_time_start),
            "totalTime": (end_time - total_time_start),
        }
    }

    output_data = convert_to_native_types(output_data)

    with open("simulation_results_v2.json", "w") as f:
        json.dump(output_data, f, indent=4)
    print("Simulation completed and results saved.")

    return output_data

