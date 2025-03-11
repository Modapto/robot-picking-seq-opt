# import json
# import copy
# from time import time
# import pandas as pd
# import numpy as np
# from configurations_final import (
#     load_distance_matrix,
#     load_containers_template,
#     load_kit_holders_template,
#     randomize_containers,
#     filter_distance_matrix
# )
# from exact_method import run_exact_tsp
# from method_linear import *
# from GraphCreation import create_directed_bipartite_graph
# from parse_json import create_distance_matrices
#
#
# def generate_unique_gr_configurations(num_configs, containers_template):
#     """
#     Generate unique random gravity rack configurations.
#     """
#     configurations = {}
#     while len(configurations) < num_configs:
#         config = randomize_containers(containers_template)
#         key = "-".join(f"{container['gr_position']}:{content['type']}" for container in config.values() for content in
#                        container["contents"])
#         if key not in configurations:
#             configurations[key] = config
#     return configurations
#
#
# def generate_kh_configuration(kh_setup, kit_holders_template):
#     """
#     Generate kit holder configuration based on the given setup.
#     Handles empty positions with the placeholder "EMPTY".
#     """
#     configured_kh = {}
#     for idx, kh_id in enumerate(kh_setup, start=1):
#         if kh_id == "EMPTY":
#             continue
#         if kh_id in kit_holders_template:
#             kh_data = copy.deepcopy(kit_holders_template[kh_id])
#             for i, content in enumerate(kh_data["contents"], start=1):
#                 content["position"] = f"{idx}.{i}"
#             configured_kh[f"KH{idx}"] = {
#                 "kh_position": str(idx),
#                 "contents": kh_data["contents"]
#             }
#         else:
#             raise ValueError(f"Kit holder ID {kh_id} not found.")
#     return configured_kh
#
# def calculate_linear_value(distance_matrix, configuration):
#     filtered_matrix = filter_distance_matrix(distance_matrix, configuration)
#     a_to_b_matrix = create_distance_matrices({"data": {"distanceMatrix": filtered_matrix}})
#     B, set_1, set_2 = create_directed_bipartite_graph(a_to_b_matrix)
#     tour = linear_picking(B, "0.0", "0.0.0", set_1, set_2)
#     cost, _ = total_cost(B, tour["tour"])
#     return cost
#
# def calculate_objective_value(distance_matrix, configuration, start_node="0.0", end_node="0.0.0"):
#     filtered_matrix = filter_distance_matrix(distance_matrix, configuration)
#     tour, cost, details = run_exact_tsp({"data": {"distanceMatrix": filtered_matrix, "start_node": start_node, "end_node": end_node}})
#     # Trim "0.0.0" to "0.0" if end_node is None
#     if end_node is None and tour[-1][1] == "0.0.0" and tour[-1][0] == "0.0.0":
#         tour = tour[:-2]  # Remove "0.0.0" to "0.0"
#         details = details[:-2]
#     return cost, tour, details
#
#
# def convert_to_native_types(data):
#     if isinstance(data, dict):
#         return {k: convert_to_native_types(v) for k, v in data.items()}
#     elif isinstance(data, list):
#         return [convert_to_native_types(v) for v in data]
#     elif isinstance(data, pd.DataFrame):
#         return data.applymap(lambda x: int(x) if isinstance(x, (np.integer, np.int32, np.int64)) else x).to_dict()
#     elif isinstance(data, (np.integer, np.int32, np.int64)):
#         return int(data)
#     else:
#         return data
#
#
# def run_simulation(input_data=None):
#     total_time_start = int(time() * 1000)
#
#     # Load input data
#     if input_data and "data" in input_data:
#         print("Remote input data received.")
#         data = input_data["data"]
#         distance_matrix = data.get("distance_matrix", load_distance_matrix())
#         containers_template = data["containers_template"]
#         kit_holders_template = data["kit_holders_template"]
#         kh_sequences = data.get("kh_sequences") or [data.get("kh_setup", [])]
#         num_random_gr_configs = data["num_random_gr_configs"]
#         current_config = data["current_config"]
#     else:
#         print("No input data provided, using fallback values.")
#         distance_matrix = load_distance_matrix()
#         containers_template = load_containers_template()
#         kit_holders_template = load_kit_holders_template()
#         kh_sequences = [["KH001", "KH002", "KH003", "KH001"], ["KH001", "KH002", "KH003", "KH002"]]
#         num_random_gr_configs = 2
#         with open("current_config.json", "r") as f:
#             current_config = json.load(f)
#
#     # Baseline full sequence with continuity
#     print("\n>>> Computing Baseline for Full Sequence...")
#     baseline_matrix = distance_matrix.copy()
#     last_node = "0.0"
#     total_exact_cost = 0
#     total_linear_cost = 0
#     full_tour = []
#     full_details = []
#
#     for i, kh_setup in enumerate(kh_sequences):
#         if i > 0:
#             print(f"Duplicating {last_node} as '0.0'...")
#             new_matrix = [edge for edge in baseline_matrix if not edge["edge"].startswith("(0.0,")]
#             for edge in distance_matrix:
#                 if edge["edge"].startswith(f"({last_node},"):
#                     new_edge = {"edge": edge["edge"].replace(f"({last_node},", "(0.0,"),
#                                 "distance": edge["distance"] + 2000}
#                     new_matrix.append(new_edge)
#             baseline_matrix = new_matrix
#
#         kh_config = generate_kh_configuration(kh_setup, kit_holders_template)
#         end_node = None if i < len(kh_sequences) - 1 else "0.0.0"
#         exact_cost, tour, details = calculate_objective_value(baseline_matrix,
#                                                               {"containers": current_config["containers"],
#                                                                "kit_holders": kh_config}, start_node="0.0",
#                                                               end_node=end_node)
#         linear_cost = calculate_linear_value(baseline_matrix,
#                                              {"containers": current_config["containers"], "kit_holders": kh_config})
#
#         total_exact_cost += exact_cost
#         total_linear_cost += linear_cost
#         full_tour.extend(tour if i == 0 else tour[1:])  # Avoid duplicating "0.0"
#         full_details.extend(details if i == 0 else [d for d in details if d["from"] != "0.0"])  # Avoid overlap
#
#         if i < len(kh_sequences) - 1:
#             last_node = tour[-1][1]  # Take the last node of the open tour
#             print(f"Last node for next sequence: {last_node}")
#
#     print(f"Baseline exact value: {total_exact_cost}")
#     print(f"Baseline linear value: {total_linear_cost}")
#
#     # Optimization runs
#     print("\n>>> Finding Best Configuration for Full Sequence...")
#     best_total_value = float("inf")
#     best_tour = []
#     best_details = []
#     phases = []
#
#     for run_id in range(num_random_gr_configs):
#         print(f"\n>>> Run {run_id + 1} with GR Configuration...")
#         gr_config = randomize_containers(containers_template)
#         working_matrix = distance_matrix.copy()
#         last_node_visited = "0.0"
#         total_value = 0
#         run_tour = []
#         run_details = []
#
#         for i, kh_setup in enumerate(kh_sequences):
#             if i > 0:
#                 print(f"Duplicating {last_node_visited} as '0.0'...")
#                 new_matrix = [edge for edge in working_matrix if not edge["edge"].startswith("(0.0,")]
#                 for edge in distance_matrix:
#                     if edge["edge"].startswith(f"({last_node_visited},"):
#                         new_edge = {"edge": edge["edge"].replace(f"({last_node_visited},", "(0.0,"),
#                                     "distance": edge["distance"] + 2000}
#                         new_matrix.append(new_edge)
#                 working_matrix = new_matrix
#
#             kh_config = generate_kh_configuration(kh_setup, kit_holders_template)
#             end_node = None if i < len(kh_sequences) - 1 else "0.0.0"
#             cost, tour, details = calculate_objective_value(working_matrix,
#                                                             {"containers": gr_config, "kit_holders": kh_config},
#                                                             start_node="0.0", end_node=end_node)
#             total_value += cost
#             run_tour.extend(tour if i == 0 else tour[1:])  # Avoid duplicating "0.0"
#             run_details.extend(details if i == 0 else [d for d in details if d["from"] != "0.0"])  # Avoid overlap
#
#             if i < len(kh_sequences) - 1:
#                 last_node_visited = tour[-1][1]  # Take the last node of the open tour
#
#         phases.append({
#             "exact": {
#                 "cost": total_value,
#                 "time_details": [{"from": step["from"], "to": step["to"], "distance": step["distance"]} for step in
#                                  run_details]
#             }
#         })
#         if total_value < best_total_value:
#             best_total_value = total_value
#             best_tour = run_tour
#             best_details = run_details
#
#     # Output
#     end_time = int(time() * 1000)
#     output_data = {
#         "uuid": input_data["uuid"] if input_data else "local_simulation",
#         "produced_at": int(time() * 1000),
#         "data": {
#             "phases": phases,
#             "baseline_exact_cost": total_exact_cost,
#             "baseline_linear_cost": total_linear_cost,
#             "best_total_value": best_total_value,
#             "solutionTime": (end_time - total_time_start),
#             "totalTime": (end_time - total_time_start)
#         }
#     }
#     output_data = convert_to_native_types(output_data)
#     with open("simulation_results_v2.json", "w") as f:
#         json.dump(output_data, f, indent=4)
#     print("Simulation completed and results saved.")
#     return output_data

import json
import copy
from time import time
from configurations_final import (
    load_distance_matrix,
    load_containers_template,
    load_kit_holders_template,
    randomize_containers,
    filter_distance_matrix
)
from exact_method import run_exact_tsp
from method_linear import linear_picking, total_cost
from GraphCreation import create_directed_bipartite_graph
from parse_json import create_distance_matrices


def generate_unique_gr_configurations(num_configs, containers_template):
    configurations = {}
    while len(configurations) < num_configs:
        config = randomize_containers(containers_template)
        key = "-".join(f"{container['gr_position']}:{content['type']}" for container in config.values() for content in
                       container["contents"])
        if key not in configurations:
            configurations[key] = config
    return configurations


def generate_kh_configuration(kh_setup, kit_holders_template):
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
            configured_kh[f"KH{idx}"] = {"kh_position": kh_id, "contents": []}
    return configured_kh


def calculate_full_sequence_cost(distance_matrix, configuration, method="exact"):
    working_matrix = distance_matrix.copy()
    last_node_visited = "0.0"
    total_method_cost = 0
    full_tour = []
    segmented_details = []
    kh_sequences = configuration["kh_sequences"]

    for i, kh_setup in enumerate(kh_sequences):
        print(f"\n>>> Processing KH Setup {i + 1}: {kh_setup}")
        if i > 0:
            print(f"Duplicating last visited node ({last_node_visited}) as '0.0'...")
            new_matrix = [edge for edge in working_matrix if not edge["edge"].startswith("(0.0,")]
            for edge in distance_matrix:
                if edge["edge"].startswith(f"({last_node_visited},"):
                    new_edge = {"edge": edge["edge"].replace(f"({last_node_visited},", "(0.0,"),
                                "distance": edge["distance"]}
                    new_matrix.append(new_edge)
            working_matrix = new_matrix

        kh_config = generate_kh_configuration(kh_setup, configuration["kit_holders_template"])
        filtered_matrix = filter_distance_matrix(working_matrix,
                                                 {"containers": configuration["containers"], "kit_holders": kh_config})
        end_node = None if i < len(kh_sequences) - 1 else "0.0"

        if method == "exact":
            tour, cost, time_details = run_exact_tsp(
                {"data": {"distanceMatrix": filtered_matrix, "start_node": "0.0", "end_node": end_node}})
            if i < len(kh_sequences) - 1:
                for j in range(len(tour) - 1, -1, -1):
                    if tour[j][1] == "0.0.0":
                        last_node_visited = tour[j][0]
                        tour = tour[:j]
                        time_details = [step for step in time_details if step["to"] not in ["0.0.0", "0.0"]]
                        cost = sum(step["distance"] for step in time_details)
                        break
                print(f"Trimmed tour, last node: {last_node_visited}")
        else:  # linear
            a_to_b_matrix = create_distance_matrices({"data": {"distanceMatrix": filtered_matrix}})
            B, set_1, set_2 = create_directed_bipartite_graph(a_to_b_matrix)
            tour_data = linear_picking(B, "0.0", "0.0" if i == len(kh_sequences) - 1 else None, set_1, set_2)
            cost, time_details = total_cost(B, tour_data["tour"])
            # Normalize time_details to use "distance" instead of "totalTime"
            time_details = [{"from": step["from"], "to": step["to"], "distance": step["totalTime"]} for step in
                            time_details]
            tour = [(step["from"], step["to"]) for step in time_details]
            if i < len(kh_sequences) - 1:
                for j in range(len(tour) - 1, -1, -1):
                    if tour[j][1] == "0.0.0":
                        last_node_visited = tour[j][0]
                        if last_node_visited == "0.0" and j > 0:  # Use previous node if "0.0"
                            last_node_visited = tour[j - 1][0]
                        tour = tour[:j]
                        time_details = [step for step in time_details if step["to"] not in ["0.0.0", "0.0"]]
                        cost = sum(step["distance"] for step in time_details)
                        break
                print(f"Trimmed linear tour, last node: {last_node_visited}")

        total_method_cost += cost
        full_tour.extend(
            tour if i == 0 else [(last_node_visited, step[1]) if step[0] == "0.0" else step for step in tour[1:]])
        segment_details = time_details if i == 0 else [
                                                          {"from": last_node_visited, "to": time_details[0]["to"],
                                                           "distance": time_details[0]["distance"]}
                                                      ] + [step for step in time_details[1:]]
        segmented_details.append(segment_details)

    return total_method_cost, full_tour, segmented_details


def run_simulation(input_data=None):
    total_time_start = int(time() * 1000)

    # Load input data
    if input_data and "data" in input_data:
        print("Remote input data received.")
        data = input_data["data"]
        distance_matrix = data.get("distance_matrix", load_distance_matrix())
        containers_template = data["containers_template"]
        kit_holders_template = data["kit_holders_template"]
        kh_sequences = data.get("kh_sequences") or [data.get("kh_setup", [])]
        num_random_gr_configs = data["num_random_gr_configs"]
        current_config = data["current_config"]
        uuid = input_data["uuid"]
    else:
        print("No input data provided, using fallback values.")
        distance_matrix = load_distance_matrix()
        containers_template = load_containers_template()
        kit_holders_template = load_kit_holders_template()
        kh_sequences = [["KH001", "KH002", "KH003", "KH001"], ["KH003", "KH002", "KH001", "KH002"]]
        num_random_gr_configs = 2
        with open("current_config.json", "r") as f:
            current_config = json.load(f)
        uuid = "local_simulation"

    # Baseline computation
    print("\n>>> Computing Baseline for Full Sequence...")
    baseline_config = {
        "containers": current_config["containers"],
        "kit_holders_template": kit_holders_template,
        "kh_sequences": kh_sequences
    }
    baseline_exact_cost, baseline_exact_tour, baseline_exact_details = calculate_full_sequence_cost(distance_matrix,
                                                                                                    baseline_config,
                                                                                                    method="exact")
    baseline_linear_cost, baseline_linear_tour, baseline_linear_details = calculate_full_sequence_cost(distance_matrix,
                                                                                                       baseline_config,
                                                                                                       method="linear")
    print(f"Baseline exact value: {baseline_exact_cost}")
    print(f"Baseline linear value: {baseline_linear_cost}")

    # Optimization runs
    print("\n>>> Finding Best Configuration for Full Sequence...")
    best_total_value = float("inf")
    runs = []

    for run_id in range(num_random_gr_configs):
        print(f"\n>>> Run {run_id + 1} with GR Configuration...")
        gr_config = randomize_containers(containers_template)
        run_config = {
            "containers": gr_config,
            "kit_holders_template": kit_holders_template,
            "kh_sequences": kh_sequences
        }
        cost, tour, segmented_details = calculate_full_sequence_cost(distance_matrix, run_config, method="exact")

        improvement_exact = round(((baseline_exact_cost - cost) / baseline_exact_cost) * 100,
                                  3) if baseline_exact_cost > 0 else 0
        improvement_linear = round(((baseline_linear_cost - cost) / baseline_linear_cost) * 100,
                                   3) if baseline_linear_cost > 0 else 0
        gr_key = "-".join(
            f"{container['gr_position']}:{content['type']}" for container in gr_config.values() for content in
            container["contents"])

        runs.append({
            "exact_cost": cost,
            "time_details": [
                [{"from": step["from"], "to": step["to"], "distance": step["distance"]} for step in segment]
                for segment in segmented_details
            ],
            "improvement_exact": improvement_exact,
            "improvement_linear": improvement_linear,
            "gr_configuration": {
                "key": gr_key,
                "config": gr_config
            }
        })
        if cost < best_total_value:
            best_total_value = cost

    # Output
    end_time = int(time() * 1000)
    output_data = {
        "uuid": uuid,
        "produced_at": int(time() * 1000),
        "data": {
            "baseline": {
                "exact": {
                    "cost": baseline_exact_cost,
                    "time_details": [
                        [{"from": step["from"], "to": step["to"], "distance": step["distance"]} for step in segment]
                        for segment in baseline_exact_details
                    ]
                },
                "linear": {
                    "cost": baseline_linear_cost,
                    "time_details": [
                        [{"from": step["from"], "to": step["to"], "distance": step["distance"]} for step in segment]
                        for segment in baseline_linear_details
                    ]
                }
            },
            "runs": runs,
            "best_total_value": best_total_value,
            "solutionTime": (end_time - total_time_start),
            "totalTime": (end_time - total_time_start)
        }
    }
    output_data = convert_to_native_types(output_data)
    with open("simulation_results_v2.json", "w") as f:
        json.dump(output_data, f, indent=4)
    print("Simulation completed and results saved.")
    return output_data


def convert_to_native_types(data):
    if isinstance(data, dict):
        return {k: convert_to_native_types(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_to_native_types(v) for v in data]
    elif isinstance(data, (int, float, str, bool)) or data is None:
        return data
    return str(data)



