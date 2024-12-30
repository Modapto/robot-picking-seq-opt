import json
import copy
# Load the existing distance matrix
with open('extended_distance_matrix.json', 'r') as f:
    distance_matrix = json.load(f)

# Containers dictionary
containers = {
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

# Kit Holders dictionary
kit_holders = {
    "KH001": {"kh_position": "1",
              "contents": [{"position": "1.1", "type": "Component_5"},
                           {"position": "1.2", "type": "Component_15"},
                           {"position": "1.3", "type": "Component_3"},
                           {"position": "1.4", "type": "Component_16"},
                           {"position": "1.5", "type": "Component_14"},
                           {"position": "1.6", "type": "Component_11"}]},
    "KH002": {"kh_position": "2",
              "contents": [{"position": "2.1", "type": "Component_4"},
                           {"position": "2.2", "type": "Component_2"},
                           {"position": "2.3", "type": "Component_12"},
                           {"position": "2.4", "type": "Component_10"}]},
    "KH003": {"kh_position": "3",
              "contents": [{"position": "3.1", "type": "Component_9"},
                           {"position": "3.2", "type": "Component_13"},
                           {"position": "3.3", "type": "Component_1"},
                           {"position": "3.4", "type": "Component_7"},
                           {"position": "3.5", "type": "Component_10"}]},
    # "KH004": {"kh_position": "4",
    #           "contents": [{"position": "4.1", "type": "Component_5"},
    #                        {"position": "4.2", "type": "Component_15"},
    #                        {"position": "4.3", "type": "Component_3"},
    #                        {"position": "4.4", "type": "Component_16"},
    #                        {"position": "4.5", "type": "Component_14"},
    #                        {"position": "4.6", "type": "Component_11"}]},
}

def filter_distance_matrix(matrix, containers, kit_holders):
    filtered_matrix = {}

    # Add edges from 0.0 to all nodes (gravity racks and kit holders)
    filtered_matrix["0.0"] = matrix["0.0"]

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
                            valid_connections.append({"node": kit_position, "distance": distance})

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
            filtered_matrix[kit_position].extend(matrix.get(kit_position, []))

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

filtered_matrix = filter_distance_matrix(distance_matrix, containers, kit_holders)

# Save the filtered matrix to a file
with open("mapping_instances_v2.json", "w") as f:
    json.dump(filtered_matrix, f, indent=4)

print("Filtered distance matrix saved successfully.")


