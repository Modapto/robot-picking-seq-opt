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


import json
import copy
from time import time
from configurations_final import (
    load_distance_matrix,
    load_containers_template,
    load_kit_holders_template,
    filter_distance_matrix,
    randomize_containers
)
from exact_method import run_exact_tsp
from method_linear import linear_picking
from GraphCreation import create_directed_bipartite_graph
from parse_json import create_distance_matrices


def run_simulation(input_data=None):
    """
    Run the simulation process with proper start/end node handling.
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
        print("No input data provided, using fallback values.")
        distance_matrix = load_distance_matrix()
        containers_template = load_containers_template()
        kit_holders_template = load_kit_holders_template()
        kh_sequences = [["KH001", "KH002", "KH003", "KH001"]]
        num_random_gr_configs = 2
        with open("current_config.json", "r") as f:
            current_config = json.load(f)

    # Initial start/end nodes
    start_node = "0.0"
    end_node = "0.0.0"
    last_node_visited = start_node

    ### **Step 1: Compute Baseline Results**
    print("\n>>> Running Baseline Configuration...")
    baseline_results = []

    for i, kh_setup in enumerate(kh_sequences):
        print(f"\n>>> Running Baseline Phase {i + 1} with KH Setup: {kh_setup}")

        # Adjust start node for sequence continuity
        if i > 0 and last_node_visited in kit_holders_template:
            print(f"✅ Setting start node to last visited KH: {last_node_visited}")
            kh_setup = [last_node_visited] + kh_setup

        # Generate KH configuration
        kh_config = generate_kh_configuration(kh_setup, kit_holders_template)

        # Filter distance matrix
        filtered_matrix = filter_distance_matrix(distance_matrix, {
            "containers": current_config["containers"],
            "kit_holders": kh_config
        })

        # Parse distance matrix and create bipartite graph
        a_to_b_matrix = create_distance_matrices({"data": {"distanceMatrix": filtered_matrix}})
        B, set_1, set_2 = create_directed_bipartite_graph(a_to_b_matrix)

        # Compute baseline cost
        exact_cost, linear_cost = None, None

        # **Run Exact Method**
        exact_tour, exact_cost, _ = run_exact_tsp({
            "data": {"distanceMatrix": filtered_matrix, "start_node": start_node, "end_node": end_node}
        })

        # **Run Linear Method**
        linear_tour = linear_picking(B, start_node, end_node, set_1, set_2)
        linear_cost, _ = total_cost(B, linear_tour["tour"])

        # **Store results**
        baseline_results.append({
            "phase": i + 1,
            "kh_setup": kh_setup,
            "current_value_exact": exact_cost,
            "current_value_linear": linear_cost
        })

        # **Update last visited node for next phase**
        if exact_tour:
            last_node_visited = exact_tour[-2][1]  # Store last real node before reaching 0.0.0
            print(f"✔️ Last visited KH updated to {last_node_visited}")

    print("\n✅ Baseline Results Computed Successfully!")

    ### **Step 2: Run Optimization With Different GR Configurations**
    print("\n>>> Running Optimization With Different GR Configurations...")
    best_total_value = float("inf")
    overall_results = []

    for run_id in range(num_random_gr_configs):
        print(f"\n>>> Running Simulation with GR Configuration {run_id + 1}...")

        # Generate new GR configuration
        gr_config = randomize_containers(containers_template)

        sequence_results = []
        last_node_visited = start_node  # Reset for new configuration

        for i, kh_setup in enumerate(kh_sequences):
            print(f"\n>>> Running Simulation Phase {i + 1} with KH Setup: {kh_setup}")

            # Adjust start node for sequence continuity
            if i > 0 and last_node_visited in kit_holders_template:
                print(f"✅ Setting start node to last visited KH: {last_node_visited}")
                kh_setup = [last_node_visited] + kh_setup

            # Generate KH configuration
            kh_config = generate_kh_configuration(kh_setup, kit_holders_template)

            # Filter distance matrix
            filtered_matrix = filter_distance_matrix(distance_matrix, {
                "containers": gr_config,
                "kit_holders": kh_config
            })

            # Parse distance matrix and create bipartite graph
            a_to_b_matrix = create_distance_matrices({"data": {"distanceMatrix": filtered_matrix}})
            B, set_1, set_2 = create_directed_bipartite_graph(a_to_b_matrix)

            # Compute cost using Exact Method
            exact_tour, exact_cost, _ = run_exact_tsp({
                "data": {"distanceMatrix": filtered_matrix, "start_node": start_node, "end_node": end_node}
            })

            # Store results
            sequence_results.append({
                "phase": i + 1,
                "kh_setup": kh_setup,
                "objective_value": exact_cost
            })

            # Update last visited node for next phase
            if exact_tour:
                last_node_visited = exact_tour[-2][1]  # Store last real node before reaching 0.0.0
                print(f"✔️ Last visited KH updated to {last_node_visited}")

        total_value = sum(res["objective_value"] for res in sequence_results)

        # Track best configuration
        if total_value < best_total_value:
            best_total_value = total_value
            best_gr_config = gr_config

        overall_results.append({
            "gr_config": gr_config,
            "total_value": total_value,
            "sequence_results": sequence_results
        })

    ### **Final Output**
    output_data = {
        "uuid": input_data["uuid"],
        "produced_at": int(time() * 1000),
        "data": {
            "baseline_results": baseline_results,
            "best_total_value": best_total_value,
            "overall_results": overall_results,
            "solutionTime": (int(time() * 1000) - total_time_start)
        }
    }

    output_data = convert_to_native_types(output_data)

    # **Save results**
    with open("simulation_results_v2.json", "w") as f:
        json.dump(output_data, f, indent=4)

    print("\n✅ Simulation Completed and Results Saved!")
    return output_data


