import random
import copy
from itertools import product
import json
import uuid
from time import *
import json

def load_distance_matrix(file_path="final_distance_matrix_dual.json"):
    """
    Load the distance matrix from a JSON file.
    """
    with open(file_path, "r") as f:
        return json.load(f)

def load_containers_template(file_path="containers_template_dual.json"):
    """
    Load the containers template from a JSON file.
    """
    with open(file_path, "r") as f:
        return json.load(f)

def load_kit_holders_template(file_path="kit_holders_template_dual.json"):
    """
    Load the kit holders template from a JSON file.
    """
    with open(file_path, "r") as f:
        return json.load(f)

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

# def filter_distance_matrix(matrix, random_config):
#     filtered_matrix = []
#     containers = random_config["containers"]
#     kit_holders = random_config["kit_holders"]
#
#     # # Transform distance matrix to a lookup dictionary
#     # matrix_dict = {}
#     # for entry in matrix:
#     #     edge = entry["edge"].strip("()").split(", ")
#     #     source, target = edge[0], edge[1]
#     #     if source not in matrix_dict:
#     #         matrix_dict[source] = {}
#     #     matrix_dict[source][target] = entry["distance"]
#
#     # Transform distance matrix to a lookup dictionary (robust against spacing)
#     matrix_dict = {}
#     for entry in matrix:
#         edge_str = entry["edge"].strip("()")
#         source, target = [x.strip() for x in edge_str.split(",")]
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
#     # Add KH → GR (KH → all gravity rack positions)
#     for kh_data in kit_holders.values():
#         for kh_content in kh_data["contents"]:
#             kh_pos = kh_content["position"]
#             if kh_pos in matrix_dict:
#                 for target, distance in matrix_dict[kh_pos].items():
#                     if target.startswith("1.") or target.startswith("2."):
#                         filtered_matrix.append({
#                             "edge": f"({kh_pos}, {target})",
#                             "distance": distance + 2000
#                         })
#
#     # Add GR → GR (between all gravity rack positions)
#     for gr_a in containers.values():
#         for a_content in gr_a["contents"]:
#             pos_a = a_content["position"]
#             if pos_a in matrix_dict:
#                 for gr_b in containers.values():
#                     for b_content in gr_b["contents"]:
#                         pos_b = b_content["position"]
#                         if pos_a != pos_b and pos_b in matrix_dict[pos_a]:
#                             filtered_matrix.append({
#                                 "edge": f"({pos_a}, {pos_b})",
#                                 "distance": matrix_dict[pos_a][pos_b] + 2000
#                             })
#
#     # ✅ Add KH → KH (active only, excluding self-loops)
#     kh_positions = []
#     for kh_data in kit_holders.values():
#         for content in kh_data["contents"]:
#             kh_positions.append(content["position"])
#
#     # Add edges: KH → KH (restricted to active KH positions only)
#     for kh1 in kh_positions:
#         for kh2 in kh_positions:
#             if kh1 == kh2:
#                 continue
#             distance = matrix_dict.get(kh1, {}).get(kh2)
#             if distance is None:
#                 distance = matrix_dict.get(kh2, {}).get(kh1)
#             if distance is not None and distance < 1000000:
#                 filtered_matrix.append({
#                     "edge": f"({kh1}, {kh2})",
#                     "distance": distance + 2000
#                 })
#
#     return filtered_matrix


def filter_distance_matrix(matrix, random_config):
    filtered_matrix = []
    containers = random_config["containers"]
    kit_holders = random_config["kit_holders"]

    # Transform distance matrix to a lookup dictionary (robust against spacing)
    matrix_dict = {}
    for entry in matrix:
        edge_str = entry["edge"].strip("()")
        source, target = [x.strip() for x in edge_str.split(",")]
        if source not in matrix_dict:
            matrix_dict[source] = {}
        matrix_dict[source][target] = entry["distance"]

    # Track active KH positions for later filtering
    kh_positions = []
    for kh_data in kit_holders.values():
        for content in kh_data["contents"]:
            kh_positions.append(content["position"])
    print(f"✅ Active KH Positions: {kh_positions}")

    # Add edges: 0.0 → all gravity racks
    if "0.0" in matrix_dict:
        for target, distance in matrix_dict["0.0"].items():
            filtered_matrix.append({"edge": f"(0.0, {target})", "distance": distance + 2000})

    # Add edge: 0.0.0 → 0.0
    if "0.0.0" in matrix_dict and "0.0" in matrix_dict["0.0.0"]:
        filtered_matrix.append({"edge": "(0.0.0, 0.0)", "distance": matrix_dict["0.0.0"]["0.0"]})

    # Add edges: KH → 0.0.0
    for pos in kh_positions:
        if pos in matrix_dict and "0.0.0" in matrix_dict[pos]:
            filtered_matrix.append({"edge": f"({pos}, 0.0.0)", "distance": matrix_dict[pos]["0.0.0"] + 2000})

    # Add edges: GR → KH (component-based)
    for container in containers.values():
        for gr_content in container["contents"]:
            for kh_data in kit_holders.values():
                for kh_content in kh_data["contents"]:
                    if kh_content["type"] == gr_content["type"]:
                        source = gr_content["position"]
                        target = kh_content["position"]
                        if source in matrix_dict and target in matrix_dict[source]:
                            filtered_matrix.append({
                                "edge": f"({source}, {target})",
                                "distance": matrix_dict[source][target] + 2000
                            })

    # Add edges: KH → GR
    for kh_data in kit_holders.values():
        for kh_content in kh_data["contents"]:
            source = kh_content["position"]
            if source in matrix_dict:
                for target, distance in matrix_dict[source].items():
                    if target.startswith("1.") or target.startswith("2."):
                        filtered_matrix.append({
                            "edge": f"({source}, {target})",
                            "distance": distance + 2000
                        })

    # Add edges: GR → GR
    for gr_a in containers.values():
        for content_a in gr_a["contents"]:
            pos_a = content_a["position"]
            if pos_a in matrix_dict:
                for gr_b in containers.values():
                    for content_b in gr_b["contents"]:
                        pos_b = content_b["position"]
                        if pos_a != pos_b and pos_b in matrix_dict[pos_a]:
                            filtered_matrix.append({
                                "edge": f"({pos_a}, {pos_b})",
                                "distance": matrix_dict[pos_a][pos_b] + 2000
                            })

    # Add edges: KH → KH (only among active KH positions)
    for kh1 in kh_positions:
        for kh2 in kh_positions:
            if kh1 == kh2:
                continue
            distance = matrix_dict.get(kh1, {}).get(kh2)
            if distance is None:
                distance = matrix_dict.get(kh2, {}).get(kh1)
            if distance is not None and distance < 1000000:
                filtered_matrix.append({
                    "edge": f"({kh1}, {kh2})",
                    "distance": distance + 2000
                })

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