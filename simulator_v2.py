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
from method_linear import linear_picking
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
    Run the simulation process, handling multiple phases of KH sequences
    and evaluating multiple GR configurations across all sequences in a structured manner.
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
        print("Input data not provided, using local files.")
        distance_matrix = load_distance_matrix()
        containers_template = load_containers_template()
        kit_holders_template = load_kit_holders_template()
        kh_sequences = [["KH001", "KH002", "KH001", "KH003"]]
        num_random_gr_configs = 2
        with open("current_config.json", "r") as f:
            current_config = json.load(f)

    # Generate multiple GR configurations
    gr_configs = generate_unique_gr_configurations(num_random_gr_configs, containers_template)

    best_config = None
    best_value = float("inf")
    overall_results = []

    for gr_key, gr_config in gr_configs.items():
        print(f"\n>>> Running Simulation for GR Configuration: {gr_key}")

        # Store results per full KH sequence
        sequence_results = []
        last_node_visited = "0.0"

        for i, kh_setup in enumerate(kh_sequences):
            print(f"\n>>> Running Phase {i + 1} with KH Setup: {kh_setup}")

            # Ensure last visited node is added explicitly
            if i > 0:
                print(f"Adding previously visited node ({last_node_visited}) to KH setup for Phase {i + 1}.")
                kh_setup = [last_node_visited] + kh_setup

            kh_config = generate_kh_configuration(kh_setup, kit_holders_template)

            # Evaluate the GR configuration for this KH setup
            obj_value = calculate_objective_value(distance_matrix, {
                "containers": gr_config,
                "kit_holders": kh_config
            })

            sequence_results.append({
                "phase": i + 1,
                "kh_setup": kh_setup,
                "objective_value": obj_value
            })

            last_node_visited = kh_setup[-1]  # Store last visited node for next phase

        total_value = sum(result["objective_value"] for result in sequence_results)

        # Store best GR configuration across full KH sequences
        if total_value < best_value:
            best_value = total_value
            best_config = gr_config

        overall_results.append({
            "gr_config": gr_key,
            "total_value": total_value,
            "sequence_results": sequence_results
        })

    end_time = int(time() * 1000)

    output_data = {
        "uuid": input_data['uuid'],
        "produced_at": int(time() * 1000),
        "data": {
            "best_config": best_config,
            "best_total_value": best_value,
            "overall_results": overall_results,
            "solutionTime": (end_time - total_time_start),
        }
    }

    output_data = convert_to_native_types(output_data)

    with open("simulation_results_v2.json", "w") as f:
        json.dump(output_data, f, indent=4)
    print("Simulation completed and results saved.")

    return output_data
