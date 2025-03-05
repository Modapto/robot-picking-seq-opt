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
    """
    Run the simulation process, handling multiple phases of KH sequences.
    """

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
        raise ValueError("Input data is required.")

    # Store simulation results
    overall_results = []

    # **STEP 1: Compute baseline values for the initial GR configuration**
    print("\n>>> Evaluating Baseline Configuration...")

    baseline_values = []
    for i, kh_setup in enumerate(kh_sequences):
        kh_config = generate_kh_configuration(kh_setup, kit_holders_template)

        baseline_exact = calculate_objective_value(distance_matrix, {
            "containers": current_config["containers"],
            "kit_holders": kh_config
        })

        baseline_linear = calculate_linear_value(distance_matrix, {
            "containers": current_config["containers"],
            "kit_holders": kh_config
        })

        baseline_values.append({
            "phase": i + 1,
            "kh_setup": kh_setup,
            "current_value_exact": baseline_exact,
            "current_value_linear": baseline_linear
        })

    # **STEP 2: Iterate Over Random GR Configurations**
    for run_idx in range(num_random_gr_configs):
        print(f"\n>>> Running Simulation with GR Configuration {run_idx + 1}")

        # Generate a new GR configuration (same for all KH sequences)
        gr_config = randomize_containers(containers_template)

        sequence_results = []
        last_node_visited = "0.0"
        total_value = 0

        for i, kh_setup in enumerate(kh_sequences):
            print(f"\n>>> Running Phase {i + 1} with KH Setup: {kh_setup}")

            # Copy KH setup and ensure last node is inserted (avoid duplication)
            kh_setup_copy = list(kh_setup)
            if i > 0 and last_node_visited not in kh_setup_copy:
                kh_setup_copy.insert(0, last_node_visited)

            kh_config = generate_kh_configuration(kh_setup_copy, kit_holders_template)

            obj_value = calculate_objective_value(distance_matrix, {
                "containers": gr_config,
                "kit_holders": kh_config
            })

            total_value += obj_value

            sequence_results.append({
                "phase": i + 1,
                "kh_setup": kh_setup_copy,
                "objective_value": obj_value
            })

            last_node_visited = kh_setup_copy[-1]  # Store last visited node for next phase

        overall_results.append({
            "gr_config": "-".join([f"{c['gr_position']}:{c['contents'][0]['type']}" for c in gr_config.values()]),
            "total_value": total_value,
            "sequence_results": sequence_results
        })

    # **STEP 3: Select the Best GR Configuration**
    best_run = min(overall_results, key=lambda x: x["total_value"])
    best_gr_config = best_run["gr_config"]
    best_total_value = best_run["total_value"]

    # **STEP 4: Compute Improvement Metrics**
    improvement_exact = round(((sum([b["current_value_exact"] for b in baseline_values]) - best_total_value) /
                               sum([b["current_value_exact"] for b in baseline_values])) * 100, 3)
    improvement_linear = round(((sum([b["current_value_linear"] for b in baseline_values]) - best_total_value) /
                                sum([b["current_value_linear"] for b in baseline_values])) * 100, 3)

    # **STEP 5: Store Final Results**
    end_time = int(time() * 1000)
    output_data = {
        "uuid": input_data['uuid'],
        "produced_at": int(time() * 1000),
        "data": {
            "baseline_results": baseline_values,
            "best_total_value": best_total_value,
            "improvement_exact": improvement_exact,
            "improvement_linear": improvement_linear,
            "overall_results": overall_results,
            "solutionTime": (end_time - total_time_start)
        }
    }

    output_data = convert_to_native_types(output_data)

    # Save to JSON file
    with open("simulation_results_v2.json", "w") as f:
        json.dump(output_data, f, indent=4)
    print("Simulation completed and results saved.")

    return output_data

