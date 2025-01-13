import random
import copy
from itertools import product
import json
import uuid
from time import *

# Load the existing distance matrix
with open('final_distance_matrix.json', 'r') as f:
    distance_matrix = json.load(f)

# Debugging: Print the type and structure of distance_matrix
print("Type of distance_matrix:", type(distance_matrix))
if isinstance(distance_matrix, list):
    print("Sample entry:", distance_matrix[0])

# Load container and kit holder templates
with open("containers_template.json", "r") as f:
    containers_template = json.load(f)

with open("kit_holders_template.json", "r") as f:
    kit_holders_template = json.load(f)

def generate_all_kh_configurations(kit_holders, num_positions=4):
    kh_keys = list(kit_holders.keys())
    all_combinations = list(product(kh_keys, repeat=num_positions))  # Cartesian product
    random.shuffle(all_combinations)  # Randomize configurations
    return all_combinations

def randomize_kit_holders(kit_holders, configuration):
    new_kit_holders = {}
    for pos_idx, kh_key in enumerate(configuration, start=1):
        kh_data = copy.deepcopy(kit_holders[kh_key])
        new_contents = []

        for i, content in enumerate(kh_data["contents"], start=1):
            content["position"] = f"{pos_idx}.{i}"
            new_contents.append(content)

        new_kit_holders[f"KH{pos_idx}"] = {
            "kh_position": str(pos_idx),
            "contents": new_contents,
        }

    return new_kit_holders

def randomize_containers(containers_template):
    all_components = []
    for container in containers_template.values():
        for content in container["contents"]:
            if content["type"] not in all_components:
                all_components.append(content["type"])

    random.shuffle(all_components)

    new_containers = {}
    for idx, container_key in enumerate(containers_template.keys(), start=1):
        group = 1 if idx <= 7 else 2
        subgroup = idx if group == 1 else idx - 7
        gr_position = f"{group}.{subgroup}"

        component_type = all_components[(idx - 1) % len(all_components)]
        new_contents = [
            {"position": f"{gr_position}.{i}", "type": component_type}
            for i in range(1, 5)
        ]

        new_containers[container_key] = {"gr_position": gr_position, "contents": new_contents}

    return new_containers

def generate_random_configuration(containers, kit_holders):
    all_kh_configs = generate_all_kh_configurations(kit_holders, num_positions=4)
    selected_config = random.choice(all_kh_configs)
    randomized_kit_holders = randomize_kit_holders(kit_holders, selected_config)
    randomized_containers = randomize_containers(containers)
    return {"containers": randomized_containers, "kit_holders": randomized_kit_holders}

def filter_distance_matrix(matrix, random_config):
    filtered_matrix = []
    containers = random_config["containers"]
    kit_holders = random_config["kit_holders"]

    # Transform distance matrix to a lookup dictionary
    matrix_dict = {}
    for entry in matrix:
        edge = entry["edge"].strip("()").split(", ")
        source, target = edge[0], edge[1]
        if source not in matrix_dict:
            matrix_dict[source] = {}
        matrix_dict[source][target] = entry["distance"]

    # Add edges: 0.0 to all gravity racks
    if "0.0" in matrix_dict:
        for target, distance in matrix_dict["0.0"].items():
            filtered_matrix.append({"edge": f"(0.0, {target})", "distance": distance + 2000})

    # Add edges: 0.0.0 to 0.0
    if "0.0.0" in matrix_dict and "0.0" in matrix_dict["0.0.0"]:
        filtered_matrix.append({"edge": "(0.0.0, 0.0)", "distance": matrix_dict["0.0.0"]["0.0"]})

    # Add edges: Kit holders to 0.0.0
    for kh_key, kh_value in kit_holders.items():
        for kh_content in kh_value["contents"]:
            if kh_content["position"] in matrix_dict and "0.0.0" in matrix_dict[kh_content["position"]]:
                filtered_matrix.append({"edge": f"({kh_content['position']}, 0.0.0)", "distance": matrix_dict[kh_content["position"]]["0.0.0"] + 2000})

    # Add edges: Gravity racks to specific kit holders
    for container_key, container_value in containers.items():
        for cont_content in container_value["contents"]:
            for kh_key, kh_value in kit_holders.items():
                for kh_content in kh_value["contents"]:
                    if kh_content["type"] == cont_content["type"]:
                        if cont_content["position"] in matrix_dict and kh_content["position"] in matrix_dict[cont_content["position"]]:
                            filtered_matrix.append({"edge": f"({cont_content['position']}, {kh_content['position']})",
                                                    "distance": matrix_dict[cont_content["position"]][kh_content["position"]] + 2000})

    # Add edges: Kit holders to all gravity racks
    for kh_key, kh_value in kit_holders.items():
        for kh_content in kh_value["contents"]:
            if kh_content["position"] in matrix_dict:
                for target, distance in matrix_dict[kh_content["position"]].items():
                    if target.startswith("1.") or target.startswith("2."):
                        filtered_matrix.append({"edge": f"({kh_content['position']}, {target})", "distance": distance + 2000})

    return filtered_matrix

# Methods for the robot
methods = ["exact", "nearest", "2-opt", "q_learning", "ql-nearest", "ql-2-opt"]
def generate_json_input(filtered_matrix):
    random_json_input = {
        "route": "robot-pick-seq-opt",
        "uuid": str(uuid.uuid4()),
        "generated_at": int(time()),
        "data": {
            "method": random.choice(methods),
            "start_node": "0.0",
            "end_node": "0.0.0",
            "distanceMatrix": filtered_matrix
        }
    }
    return random_json_input

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
# with open("configurations_final.json", "w") as f:
#     json.dump(random_json_input, f, indent=4)
#
# with open("configuration_final_sample.json", "w") as f:
#     json.dump(random_config, f, indent=4)
#
# print("Filtered distance matrix and random configuration saved successfully.")