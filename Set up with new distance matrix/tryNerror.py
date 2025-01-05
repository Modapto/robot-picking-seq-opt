# import random
# import copy
# from itertools import product
# import json
# import uuid
# from time import *
#
# # Load the existing distance matrix
# with open('final_distance_matrix.json', 'r') as f:
#     distance_matrix = json.load(f)
#
# # Debugging: Print the type and structure of distance_matrix
# print("Type of distance_matrix:", type(distance_matrix))
# if isinstance(distance_matrix, list):
#     print("Sample entry:", distance_matrix[0])
#
# # kit holders and containers
# kit_holders_template = {
#     "KH001": {"contents": [{"position": "", "type": "Component_5"},
#                            {"position": "", "type": "Component_15"},
#                            {"position": "", "type": "Component_3"},
#                            {"position": "", "type": "Component_16"},
#                            {"position": "", "type": "Component_14"},
#                            {"position": "", "type": "Component_11"}]},
#     "KH002": {"contents": [{"position": "", "type": "Component_4"},
#                            {"position": "", "type": "Component_2"},
#                            {"position": "", "type": "Component_12"},
#                            {"position": "", "type": "Component_10"}]},
#     "KH003": {"contents": [{"position": "", "type": "Component_9"},
#                            {"position": "", "type": "Component_13"},
#                            {"position": "", "type": "Component_1"},
#                            {"position": "", "type": "Component_7"},
#                            {"position": "", "type": "Component_10"}]}
# }
#
# containers_template = {
#     "Container_1": {"gr_position": "1.1","contents" : [{"position":"1.1.1","type":"Component_1"},
#                                                        {"position":"1.1.2","type":"Component_1"},
#                                                        {"position":"1.1.3","type":"Component_1"},
#                                                        {"position":"1.1.4","type":"Component_1"}]},
#     "Container_2": {"gr_position": "1.2","contents" : [{"position":"1.2.1","type":"Component_2"},
#                                                        {"position":"1.2.2","type":"Component_2"},
#                                                        {"position":"1.2.3","type":"Component_2"},
#                                                        {"position":"1.2.4","type":"Component_2"}]},
#     "Container_3": {"gr_position": "1.3", "contents": [{"position": "1.3.1", "type": "Component_3"},
#                                                        {"position": "1.3.2", "type": "Component_3"},
#                                                        {"position": "1.3.3", "type": "Component_3"},
#                                                        {"position": "1.3.4", "type": "Component_3"}]},
#     "Container_4": {"gr_position": "1.4", "contents": [{"position": "1.4.1", "type": "Component_4"},
#                                                        {"position": "1.4.2", "type": "Component_4"},
#                                                        {"position": "1.4.3", "type": "Component_4"},
#                                                        {"position": "1.4.4", "type": "Component_4"}]},
#     "Container_5": {"gr_position": "1.5", "contents": [{"position": "1.5.1", "type": "Component_5"},
#                                                        {"position": "1.5.2", "type": "Component_5"},
#                                                        {"position": "1.5.3", "type": "Component_5"},
#                                                        {"position": "1.5.4", "type": "Component_5"}]},
#     "Container_6": {"gr_position": "1.6", "contents": [{"position": "1.6.1", "type": "Component_7"},
#                                                        {"position": "1.6.2", "type": "Component_7"},
#                                                        {"position": "1.6.3", "type": "Component_7"},
#                                                        {"position": "1.6.4", "type": "Component_7"}]},
#     "Container_7": {"gr_position": "1.7", "contents": [{"position": "1.7.1", "type": "Component_9"},
#                                                        {"position": "1.7.2", "type": "Component_9"},
#                                                        {"position": "1.7.3", "type": "Component_9"},
#                                                        {"position": "1.7.4", "type": "Component_9"}]},
#     "Container_8": {"gr_position": "1.8", "contents": [{"position": "2.1.1", "type": "Component_10"},
#                                                        {"position": "2.1.2", "type": "Component_10"},
#                                                        {"position": "2.1.3", "type": "Component_10"},
#                                                        {"position": "2.1.4", "type": "Component_10"}]},
#     "Container_9": {"gr_position": "1.9", "contents": [{"position": "2.2.1", "type": "Component_11"},
#                                                        {"position": "2.2.2", "type": "Component_11"},
#                                                        {"position": "2.2.3", "type": "Component_11"},
#                                                        {"position": "2.2.4", "type": "Component_11"}]},
#     "Container_10": {"gr_position": "1.10", "contents": [{"position": "2.3.1", "type": "Component_12"},
#                                                        {"position": "2.3.2", "type": "Component_12"},
#                                                        {"position": "2.3.3", "type": "Component_12"},
#                                                        {"position": "2.3.4", "type": "Component_12"}]},
#     "Container_11": {"gr_position": "1.11", "contents": [{"position": "2.4.1", "type": "Component_13"},
#                                                        {"position": "2.4.2", "type": "Component_13"},
#                                                        {"position": "2.4.3", "type": "Component_13"},
#                                                        {"position": "2.4.4", "type": "Component_13"}]},
#     "Container_12": {"gr_position": "1.12", "contents": [{"position": "2.5.1", "type": "Component_14"},
#                                                        {"position": "2.5.2", "type": "Component_14"},
#                                                        {"position": "2.5.3", "type": "Component_14"},
#                                                        {"position": "2.5.4", "type": "Component_14"}]},
#     "Container_13": {"gr_position": "1.13", "contents": [{"position": "2.6.1", "type": "Component_15"},
#                                                        {"position": "2.6.2", "type": "Component_15"},
#                                                        {"position": "2.6.3", "type": "Component_15"},
#                                                        {"position": "2.6.4", "type": "Component_15"}]},
#     "Container_14": {"gr_position": "1.14", "contents": [{"position": "2.7.1", "type": "Component_16"},
#                                                        {"position": "2.7.2", "type": "Component_16"},
#                                                        {"position": "2.7.3", "type": "Component_16"},
#                                                        {"position": "2.7.4", "type": "Component_16"}]}
# }
#
# def generate_all_kh_configurations(kit_holders, num_positions=4):
#     kh_keys = list(kit_holders.keys())
#     all_combinations = list(product(kh_keys, repeat=num_positions))  # Cartesian product
#     random.shuffle(all_combinations)  # Randomize configurations
#     return all_combinations
#
# def randomize_kit_holders(kit_holders, configuration):
#     new_kit_holders = {}
#     for pos_idx, kh_key in enumerate(configuration, start=1):
#         kh_data = copy.deepcopy(kit_holders[kh_key])
#         new_contents = []
#
#         for i, content in enumerate(kh_data["contents"], start=1):
#             content["position"] = f"{pos_idx}.{i}"
#             new_contents.append(content)
#
#         new_kit_holders[f"KH{pos_idx}"] = {
#             "kh_position": str(pos_idx),
#             "contents": new_contents,
#         }
#
#     return new_kit_holders
#
# def randomize_containers(containers_template):
#     all_components = []
#     for container in containers_template.values():
#         for content in container["contents"]:
#             if content["type"] not in all_components:
#                 all_components.append(content["type"])
#
#     random.shuffle(all_components)
#
#     new_containers = {}
#     for idx, container_key in enumerate(containers_template.keys(), start=1):
#         group = 1 if idx <= 7 else 2
#         subgroup = idx if group == 1 else idx - 7
#         gr_position = f"{group}.{subgroup}"
#
#         component_type = all_components[(idx - 1) % len(all_components)]
#         new_contents = [
#             {"position": f"{gr_position}.{i}", "type": component_type}
#             for i in range(1, 5)
#         ]
#
#         new_containers[container_key] = {"gr_position": gr_position, "contents": new_contents}
#
#     return new_containers
#
# def generate_random_configuration(containers, kit_holders):
#     all_kh_configs = generate_all_kh_configurations(kit_holders, num_positions=4)
#     selected_config = random.choice(all_kh_configs)
#     randomized_kit_holders = randomize_kit_holders(kit_holders, selected_config)
#     randomized_containers = randomize_containers(containers)
#     return {"containers": randomized_containers, "kit_holders": randomized_kit_holders}
#
# def filter_distance_matrix(matrix, random_config):
#     filtered_matrix = []
#     containers = random_config["containers"]
#     kit_holders = random_config["kit_holders"]
#
#     # Transform distance matrix to a lookup dictionary
#     matrix_dict = {}
#     for entry in matrix:
#         edge = entry["edge"].strip("()").split(", ")
#         source, target = edge[0], edge[1]
#         if source not in matrix_dict:
#             matrix_dict[source] = {}
#         matrix_dict[source][target] = entry["distance"]
#
#     # Add edges: 0.0 to all gravity racks
#     if "0.0" in matrix_dict:
#         for target, distance in matrix_dict["0.0"].items():
#             filtered_matrix.append({"edge": f"(0.0, {target})", "distance": distance + 2000})
#
#     # Add edges: 0.0.0 to 0.0
#     if "0.0.0" in matrix_dict and "0.0" in matrix_dict["0.0.0"]:
#         filtered_matrix.append({"edge": "(0.0.0, 0.0)", "distance": matrix_dict["0.0.0"]["0.0"]})
#
#     # Add edges: Kit holders to 0.0.0
#     for kh_key, kh_value in kit_holders.items():
#         for kh_content in kh_value["contents"]:
#             if kh_content["position"] in matrix_dict and "0.0.0" in matrix_dict[kh_content["position"]]:
#                 filtered_matrix.append({"edge": f"({kh_content['position']}, 0.0.0)", "distance": matrix_dict[kh_content["position"]]["0.0.0"] + 2000})
#
#     # Add edges: Gravity racks to specific kit holders
#     for container_key, container_value in containers.items():
#         for cont_content in container_value["contents"]:
#             for kh_key, kh_value in kit_holders.items():
#                 for kh_content in kh_value["contents"]:
#                     if kh_content["type"] == cont_content["type"]:
#                         if cont_content["position"] in matrix_dict and kh_content["position"] in matrix_dict[cont_content["position"]]:
#                             filtered_matrix.append({"edge": f"({cont_content['position']}, {kh_content['position']})",
#                                                     "distance": matrix_dict[cont_content["position"]][kh_content["position"]] + 2000})
#
#     # Add edges: Kit holders to all gravity racks
#     for kh_key, kh_value in kit_holders.items():
#         for kh_content in kh_value["contents"]:
#             if kh_content["position"] in matrix_dict:
#                 for target, distance in matrix_dict[kh_content["position"]].items():
#                     if target.startswith("1.") or target.startswith("2."):
#                         filtered_matrix.append({"edge": f"({kh_content['position']}, {target})", "distance": distance + 2000})
#
#     return filtered_matrix
#
# # Methods for the robot
# methods = ["exact", "nearest", "2-opt", "q_learning", "ql-nearest", "ql-2-opt"]
# def generate_json_input(filtered_matrix):
#     random_json_input = {
#         "route": "robot-pick-seq-opt",
#         "uuid": str(uuid.uuid4()),
#         "generated_at": int(time()),
#         "data": {
#             "method": random.choice(methods),
#             "start_node": "0.0",
#             "end_node": "0.0.0",
#             "distanceMatrix": filtered_matrix
#         }
#     }
#     return random_json_input
#
# # Generate random configuration
# containers = copy.deepcopy(containers_template)
# kit_holders = copy.deepcopy(kit_holders_template)
# random_config = generate_random_configuration(containers, kit_holders)
#
# # Filter the distance matrix
# filtered_matrix = filter_distance_matrix(distance_matrix, random_config)
# # Generate the final JSON structure
# random_json_input = generate_json_input(filtered_matrix)
#
# # Save the results
# with open("final_random_configuration.json", "w") as f:
#     json.dump(random_json_input, f, indent=4)
#
# print("Filtered distance matrix and random configuration saved successfully.")

from distance_matrix_creation import *
from graph_creation import *
from exact import *

import json
import time  # Ensure the time module is imported if not already

# File path to the input JSON
json_file_path = "final_random_configuration.json"

# Open and load the JSON file
try:
    with open(json_file_path, 'r') as f:
        input_data = json.load(f)
    print(f"Local JSON input has been loaded from {json_file_path}.")
except FileNotFoundError:
    print(f"Error: The file {json_file_path} does not exist.")
    exit(1)  # Exit the script if the file is missing

# Parse the distance matrices
a_to_b_matrix = create_distance_matrices(input_data)  # Ensure this function is defined elsewhere
print(a_to_b_matrix)
print("Distance matrices created!")

# Create the bipartite graph
B, set_1, set_2 = create_directed_bipartite_graph(a_to_b_matrix)  # Ensure this function is defined
print("Graph generated!")

# Extract important fields from the input data
start_node = input_data['data'].get('start_node', '0.0')
end_node = input_data['data'].get('end_node', '0.0.0')
method = input_data['data'].get('method', 'nearest')

# Ensure the end_node is in set_2
if end_node not in set_2:
    set_2.append(end_node)

# Initialize result storage and timing
results = {}
solution_time_start = int(time.time() * 1000)  # Time in milliseconds

try:
    # Run methods based on the input's method
    if method == "exact" or method == "all":
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

# Calculate end time
end_time = int(time.time() * 1000)

# Prepare picking sequence
picking_seq = []
total_loading_time = None
for method, result in results.items():
    if "time_details" in result:
        picking_seq.append({"method": method})
        picking_seq.extend(result["time_details"])
        total_loading_time = result.get("totalLoadingTime", 0)

# Display picking sequence
print("Picking Sequence:")
import numpy as np
for pick in picking_seq:
    print(pick)

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


# Prepare the output data
output_data = {
    "uuid": input_data.get('uuid', 'unknown-uuid'),
    "produced_at": int(time.time() * 1000),
    "data": {
        "pickingSeq": time_details,
        "totalLoadingTime": exact_tour["total_cost"],
        "solutionTime": end_time - solution_time_start
    }
}

output_data = convert_to_native_types(output_data)

# Save the output to a JSON file
output_json_file_path = "exact_method_result.json"
try:
    with open(output_json_file_path, 'w') as json_file:
        json.dump(output_data, json_file, indent=4)
    print(f"Local output saved to {output_json_file_path}")
except IOError as e:
    print(f"Error saving output JSON: {e}")
