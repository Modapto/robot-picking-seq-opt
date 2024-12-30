import random
import copy
from itertools import product
import json

# Load the existing distance matrix
with open('extended_distance_matrix.json', 'r') as f:
    distance_matrix = json.load(f)

# kit holders and containers
kit_holders_template = {
    "KH001": {"contents": [{"position": "", "type": "Component_5"},
                           {"position": "", "type": "Component_15"},
                           {"position": "", "type": "Component_3"},
                           {"position": "", "type": "Component_16"},
                           {"position": "", "type": "Component_14"},
                           {"position": "", "type": "Component_11"}]},
    "KH002": {"contents": [{"position": "", "type": "Component_4"},
                           {"position": "", "type": "Component_2"},
                           {"position": "", "type": "Component_12"},
                           {"position": "", "type": "Component_10"}]},
    "KH003": {"contents": [{"position": "", "type": "Component_9"},
                           {"position": "", "type": "Component_13"},
                           {"position": "", "type": "Component_1"},
                           {"position": "", "type": "Component_7"},
                           {"position": "", "type": "Component_10"}]}
}

containers_template = {
    "Container_1": {"gr_position": "1.1","contents" : [{"position":"1.1.1","type":"Component_1"},
                                                       {"position":"1.1.2","type":"Component_1"},
                                                       {"position":"1.1.3","type":"Component_1"},
                                                       {"position":"1.1.4","type":"Component_1"}]},
    "Container_2": {"gr_position": "1.2","contents" : [{"position":"1.2.1","type":"Component_2"},
                                                       {"position":"1.2.2","type":"Component_2"},
                                                       {"position":"1.2.3","type":"Component_2"},
                                                       {"position":"1.2.4","type":"Component_2"}]},
    "Container_3": {"gr_position": "1.3", "contents": [{"position": "1.3.1", "type": "Component_3"},
                                                       {"position": "1.3.2", "type": "Component_3"},
                                                       {"position": "1.3.3", "type": "Component_3"},
                                                       {"position": "1.3.4", "type": "Component_3"}]},
    "Container_4": {"gr_position": "1.4", "contents": [{"position": "1.4.1", "type": "Component_4"},
                                                       {"position": "1.4.2", "type": "Component_4"},
                                                       {"position": "1.4.3", "type": "Component_4"},
                                                       {"position": "1.4.4", "type": "Component_4"}]},
    "Container_5": {"gr_position": "1.5", "contents": [{"position": "1.5.1", "type": "Component_5"},
                                                       {"position": "1.5.2", "type": "Component_5"},
                                                       {"position": "1.5.3", "type": "Component_5"},
                                                       {"position": "1.5.4", "type": "Component_5"}]},
    "Container_6": {"gr_position": "1.6", "contents": [{"position": "1.6.1", "type": "Component_7"},
                                                       {"position": "1.6.2", "type": "Component_7"},
                                                       {"position": "1.6.3", "type": "Component_7"},
                                                       {"position": "1.6.4", "type": "Component_7"}]},
    "Container_7": {"gr_position": "1.7", "contents": [{"position": "1.7.1", "type": "Component_9"},
                                                       {"position": "1.7.2", "type": "Component_9"},
                                                       {"position": "1.7.3", "type": "Component_9"},
                                                       {"position": "1.7.4", "type": "Component_9"}]},
    "Container_8": {"gr_position": "1.8", "contents": [{"position": "2.1.1", "type": "Component_10"},
                                                       {"position": "2.1.2", "type": "Component_10"},
                                                       {"position": "2.1.3", "type": "Component_10"},
                                                       {"position": "2.1.4", "type": "Component_10"}]},
    "Container_9": {"gr_position": "1.9", "contents": [{"position": "2.2.1", "type": "Component_11"},
                                                       {"position": "2.2.2", "type": "Component_11"},
                                                       {"position": "2.2.3", "type": "Component_11"},
                                                       {"position": "2.2.4", "type": "Component_11"}]},
    "Container_10": {"gr_position": "1.10", "contents": [{"position": "2.3.1", "type": "Component_12"},
                                                       {"position": "2.3.2", "type": "Component_12"},
                                                       {"position": "2.3.3", "type": "Component_12"},
                                                       {"position": "2.3.4", "type": "Component_12"}]},
    "Container_11": {"gr_position": "1.11", "contents": [{"position": "2.4.1", "type": "Component_13"},
                                                       {"position": "2.4.2", "type": "Component_13"},
                                                       {"position": "2.4.3", "type": "Component_13"},
                                                       {"position": "2.4.4", "type": "Component_13"}]},
    "Container_12": {"gr_position": "1.12", "contents": [{"position": "2.5.1", "type": "Component_14"},
                                                       {"position": "2.5.2", "type": "Component_14"},
                                                       {"position": "2.5.3", "type": "Component_14"},
                                                       {"position": "2.5.4", "type": "Component_14"}]},
    "Container_13": {"gr_position": "1.13", "contents": [{"position": "2.6.1", "type": "Component_15"},
                                                       {"position": "2.6.2", "type": "Component_15"},
                                                       {"position": "2.6.3", "type": "Component_15"},
                                                       {"position": "2.6.4", "type": "Component_15"}]},
    "Container_14": {"gr_position": "1.14", "contents": [{"position": "2.7.1", "type": "Component_16"},
                                                       {"position": "2.7.2", "type": "Component_16"},
                                                       {"position": "2.7.3", "type": "Component_16"},
                                                       {"position": "2.7.4", "type": "Component_16"}]}
}

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
#     filtered_matrix = {}  # Initialize filtered matrix with only required nodes
#
#     # containers and kit holders from random_config
#     containers = random_config["containers"]
#     kit_holders = random_config["kit_holders"]
#
#     for kh_key, kh_value in kit_holders.items():
#         for kh_content in kh_value["contents"]:
#             kit_position = kh_content["position"]
#             kit_component = kh_content["type"]
#
#             # Find valid connections for this kit position
#             valid_connections = []
#
#             for container_key, container_value in containers.items():
#                 for cont_content in container_value["contents"]:
#                     cont_position = cont_content["position"]
#                     cont_component = cont_content["type"]
#
#                     # Match components and retrieve distances
#                     if kit_component == cont_component:
#                         distance = get_distance_from_matrix(matrix, kit_position, cont_position)
#                         if distance is not None:
#                             valid_connections.append({"node": cont_position, "distance": distance})
#
#             # Add to filtered matrix only if there are valid connections
#             if valid_connections:
#                 filtered_matrix[kit_position] = valid_connections
#
#     return filtered_matrix
#
# def get_distance_from_matrix(matrix, kit_position, container_position):
#     """
#     Retrieve the distance between kit_position and container_position from the matrix.
#     """
#     if kit_position in matrix:
#         for entry in matrix[kit_position]:
#             if entry["node"] == container_position:
#                 return entry["distance"]
#     return None
#
# containers = copy.deepcopy(containers_template)
# kit_holders = copy.deepcopy(kit_holders_template)
#
# random_config = generate_random_configuration(containers, kit_holders)
# filtered_matrix = filter_distance_matrix(distance_matrix, random_config)
# print(random_config)
# with open("random_configuration_distance_matrix.json", "w") as f:
#     json.dump(filtered_matrix, f, indent=4)
#
# print("Filtered distance matrix saved successfully.")

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
    filtered_matrix = {}

    containers = random_config["containers"]
    kit_holders = random_config["kit_holders"]

    # Add edges from 0.0 to all nodes (gravity racks and kit holders) with extra distance
    filtered_matrix["0.0"] = [{"node": connection["node"], "distance": connection["distance"] + 2000}
                               for connection in matrix["0.0"]]


    # Add edge from 0.0.0 to 0.0
    filtered_matrix["0.0.0"] = [{"node": "0.0", "distance": 0}]

    # Add edges from kit holders to 0.0.0
    for kh_key, kh_value in kit_holders.items():
        for kh_content in kh_value["contents"]:
            kit_position = kh_content["position"]
            filtered_matrix[kit_position] = []

        # Add edges from gravity racks to their respective kit holders based on components
    for container_key, container_value in containers.items():
        for cont_content in container_value["contents"]:
            cont_position = cont_content["position"]
            cont_component = cont_content["type"]

            valid_connections = []

            for kh_key, kh_value in kit_holders.items():
                for kh_content in kh_value["contents"]:
                    kit_position = kh_content["position"]
                    kit_component = kh_content["type"]

                    # Add edge if components match
                    if kit_component == cont_component:
                        distance = get_distance_from_matrix(matrix, cont_position, kit_position)
                        if distance is not None:
                            valid_connections.append({"node": kit_position, "distance": distance + 2000})

            # Add all valid connections for this gravity rack position
            if valid_connections:
                if cont_position not in filtered_matrix:
                    filtered_matrix[cont_position] = []
                filtered_matrix[cont_position].extend(valid_connections)

        # Add edges from kit holders to all gravity racks (includes component-based filtering)
    for kh_key, kh_value in kit_holders.items():
        for kh_content in kh_value["contents"]:
            kit_position = kh_content["position"]

            if kit_position not in filtered_matrix:
                filtered_matrix[kit_position] = []

            # Add all connections to gravity racks
            for connection in matrix.get(kit_position, []):
                connection["distance"] += 2000
                filtered_matrix[kit_position].append(connection)

    return filtered_matrix

def get_distance_from_matrix(matrix, source, target):
    """
    Retrieve the distance between source and target from the matrix.
    """
    if source in matrix:
        for entry in matrix[source]:
            if entry["node"] == target:
                return entry["distance"]
    return None


containers = copy.deepcopy(containers_template)
kit_holders = copy.deepcopy(kit_holders_template)

random_config = generate_random_configuration(containers, kit_holders)
filtered_matrix = filter_distance_matrix(distance_matrix, random_config)
print(random_config)
with open("configurations_with_extra_distance.json", "w") as f:
    json.dump(filtered_matrix, f, indent=4)

print("Filtered distance matrix saved successfully.")