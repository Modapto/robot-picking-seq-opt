import json
import copy
# Load the existing distance matrix
with open('final_distance_matrix.json', 'r') as f:
    distance_matrix = json.load(f)

# Containers dictionary
containers = {
    "Container_1": {"gr_position": "1.1","contents" : [{"position":"1.1.1","type":"Component_1"},
                                                       {"position":"1.1.2","type":"Component_1"},
                                                       {"position":"1.1.3","type":"Component_1"},
                                                       {"position":"1.1.4","type":"Component_1"}]},
    "Container_2": {"gr_position": "1.2","contents" : [{"position":"1.2.1","type":"Component_9"},
                                                       {"position":"1.2.2","type":"Component_9"},
                                                       {"position":"1.2.3","type":"Component_9"},
                                                       {"position":"1.2.4","type":"Component_9"}]},
    "Container_3": {"gr_position": "1.3", "contents": [{"position": "1.3.1", "type": "Component_11"},
                                                       {"position": "1.3.2", "type": "Component_11"},
                                                       {"position": "1.3.3", "type": "Component_11"},
                                                       {"position": "1.3.4", "type": "Component_11"}]},
    "Container_4": {"gr_position": "1.4", "contents": [{"position": "1.4.1", "type": "Component_15"},
                                                       {"position": "1.4.2", "type": "Component_15"},
                                                       {"position": "1.4.3", "type": "Component_15"},
                                                       {"position": "1.4.4", "type": "Component_15"}]},
    "Container_5": {"gr_position": "1.5", "contents": [{"position": "1.5.1", "type": "Component_10"},
                                                       {"position": "1.5.2", "type": "Component_10"},
                                                       {"position": "1.5.3", "type": "Component_10"},
                                                       {"position": "1.5.4", "type": "Component_10"}]},
    "Container_6": {"gr_position": "1.6", "contents": [{"position": "1.6.1", "type": "Component_16"},
                                                       {"position": "1.6.2", "type": "Component_16"},
                                                       {"position": "1.6.3", "type": "Component_16"},
                                                       {"position": "1.6.4", "type": "Component_16"}]},
    "Container_7": {"gr_position": "1.7", "contents": [{"position": "1.7.1", "type": "Component_4"},
                                                       {"position": "1.7.2", "type": "Component_4"},
                                                       {"position": "1.7.3", "type": "Component_4"},
                                                       {"position": "1.7.4", "type": "Component_4"}]},
    "Container_8": {"gr_position": "2.1", "contents": [{"position": "2.1.1", "type": "Component_13"},
                                                       {"position": "2.1.2", "type": "Component_13"},
                                                       {"position": "2.1.3", "type": "Component_13"},
                                                       {"position": "2.1.4", "type": "Component_13"}]},
    "Container_9": {"gr_position": "2.2", "contents": [{"position": "2.2.1", "type": "Component_3"},
                                                       {"position": "2.2.2", "type": "Component_3"},
                                                       {"position": "2.2.3", "type": "Component_3"},
                                                       {"position": "2.2.4", "type": "Component_3"}]},
    "Container_10": {"gr_position": "2.3", "contents": [{"position": "2.3.1", "type": "Component_12"},
                                                        {"position": "2.3.2", "type": "Component_12"},
                                                        {"position": "2.3.3", "type": "Component_12"},
                                                        {"position": "2.3.4", "type": "Component_12"}]},
    "Container_11": {"gr_position": "2.4", "contents": [{"position": "2.4.1", "type": "Component_7"},
                                                        {"position": "2.4.2", "type": "Component_7"},
                                                        {"position": "2.4.3", "type": "Component_7"},
                                                        {"position": "2.4.4", "type": "Component_7"}]},
    "Container_12": {"gr_position": "2.5", "contents": [{"position": "2.5.1", "type": "Component_14"},
                                                        {"position": "2.5.2", "type": "Component_14"},
                                                        {"position": "2.5.3", "type": "Component_14"},
                                                        {"position": "2.5.4", "type": "Component_14"}]},
    "Container_13": {"gr_position": "2.6", "contents": [{"position": "2.6.1", "type": "Component_2"},
                                                        {"position": "2.6.2", "type": "Component_2"},
                                                        {"position": "2.6.3", "type": "Component_2"},
                                                        {"position": "2.6.4", "type": "Component_2"}]},
    "Container_14": {"gr_position": "2.7", "contents": [{"position": "2.7.1", "type": "Component_5"},
                                                        {"position": "2.7.2", "type": "Component_5"},
                                                        {"position": "2.7.3", "type": "Component_5"},
                                                        {"position": "2.7.4", "type": "Component_5"}]}
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
    "KH004": {"kh_position": "4",
              "contents": [{"position": "4.1", "type": "Component_5"},
                           {"position": "4.2", "type": "Component_15"},
                           {"position": "4.3", "type": "Component_3"},
                           {"position": "4.4", "type": "Component_16"},
                           {"position": "4.5", "type": "Component_14"},
                           {"position": "4.6", "type": "Component_11"}]},
}

# def filter_and_restructure_matrix(matrix, containers, kit_holders):
#     filtered_matrix = []
#
#     # Convert matrix to dictionary format for efficient lookup
#     matrix_dict = {}
#     for entry in matrix:
#         edge = entry['edge'].strip('()').split(", ")
#         source, target = edge
#         if source not in matrix_dict:
#             matrix_dict[source] = []
#         matrix_dict[source].append({"node": target, "distance": entry["distance"]})
#
#     # Add edges from 0.0 to all gravity racks
#     if "0.0" in matrix_dict:
#         for entry in matrix_dict["0.0"]:
#             if any(entry["node"].startswith(container["gr_position"]) for container in containers.values()):
#                 filtered_matrix.append({"edge": f"(0.0, {entry['node']})", "distance": entry["distance"]})
#
#     # Add edge from 0.0.0 to 0.0
#     if "0.0.0" in matrix_dict and "0.0" in matrix_dict:
#         for entry in matrix_dict["0.0.0"]:
#             if entry["node"] == "0.0":
#                 filtered_matrix.append({"edge": "(0.0.0, 0.0)", "distance": entry["distance"]})
#
#     # Add edges from kit holders to 0.0.0
#     for kh in kit_holders.values():
#         for kh_content in kh["contents"]:
#             if kh_content["position"] in matrix_dict and "0.0.0" in matrix_dict:
#                 for entry in matrix_dict[kh_content["position"]]:
#                     if entry["node"] == "0.0.0":
#                         filtered_matrix.append({"edge": f"({kh_content['position']}, 0.0.0)", "distance": entry["distance"]})
#
#     # Add edges between kit holders and ALL gravity racks
#     for container in containers.values():
#         for content in container["contents"]:
#             for kh in kit_holders.values():
#                 for kh_content in kh["contents"]:
#                     if kh_content["position"] in matrix_dict and content["position"] in matrix_dict:
#                         for entry in matrix_dict[kh_content["position"]]:
#                             if entry["node"] == content["position"]:
#                                 filtered_matrix.append({"edge": f"({kh_content['position']}, {content['position']})",
#                                                         "distance": entry["distance"]})
#
#     # Add edges from gravity racks to specific kit holders based on matching components
#     for container in containers.values():
#         for content in container["contents"]:
#             for kh in kit_holders.values():
#                 for kh_content in kh["contents"]:
#                     if content["position"] in matrix_dict and kh_content["position"] in matrix_dict:
#                         for entry in matrix_dict[content["position"]]:
#                             if entry["node"] == kh_content["position"] and content["type"] == kh_content["type"]:
#                                 filtered_matrix.append({"edge": f"({content['position']}, {kh_content['position']})",
#                                                         "distance": entry["distance"]})
#
#     return filtered_matrix
def filter_and_restructure_matrix(distance_matrix, containers, kit_holders):
    filtered_matrix = []

    # Transform distance matrix to a lookup dictionary
    matrix_dict = {}
    for entry in distance_matrix:
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

filtered_matrix = filter_and_restructure_matrix(distance_matrix, containers, kit_holders)

# Save the filtered matrix to a file
with open("mapping_instances.json", "w") as f:
    json.dump(filtered_matrix, f, indent=4)

print("Filtered distance matrix saved successfully.")