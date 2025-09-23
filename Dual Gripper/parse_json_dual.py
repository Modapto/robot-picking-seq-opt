# import json
# import pandas as pd
#
# def create_distance_matrices(input_data, large_number=1000000):
#     """
#     Creates a full distance matrix from the JSON input (either dict or file path).
#     Ensures all nodes are included in both rows and columns.
#     """
#
#     # Load JSON data if a filepath is given
#     if isinstance(input_data, str):
#         with open(input_data, 'r') as f:
#             input_data = json.load(f)
#     elif not isinstance(input_data, dict):
#         raise ValueError("Input must be a JSON file path or a dictionary.")
#
#     # Parse distance entries
#     distance_matrix = input_data['data']['distance_matrix']
#     a_to_b_data = {}
#     all_nodes = set()
#
#     for entry in distance_matrix:
#         edge = entry.get('edge')
#         if edge:
#             pointA, pointB = edge.strip('()').split(', ')
#             distance = entry['distance']
#
#             all_nodes.update([pointA, pointB])
#
#             if pointA not in a_to_b_data:
#                 a_to_b_data[pointA] = {}
#             a_to_b_data[pointA][pointB] = distance
#
#     # Create matrix using all known nodes
#     all_nodes = sorted(all_nodes)  # for consistent ordering
#     a_to_b_matrix = pd.DataFrame(index=all_nodes, columns=all_nodes)
#
#     for pointA, destinations in a_to_b_data.items():
#         for pointB, distance in destinations.items():
#             a_to_b_matrix.at[pointA, pointB] = distance
#
#     # Fill missing with large_number and convert to int
#     a_to_b_matrix = a_to_b_matrix.fillna(large_number).astype(int)
#
#     # Node reordering for structure (KH first, then GR)
#     kit_holders = sorted([n for n in all_nodes if len(n.split('.')) == 2 or n == '0.0'])
#     gravity_racks = sorted([n for n in all_nodes if len(n.split('.')) == 3 or n == '0.0.0'])
#     node_order = kit_holders + gravity_racks
#
#     a_to_b_matrix = a_to_b_matrix.reindex(index=node_order, columns=node_order, fill_value=large_number)
#
#     print(f"✅ Distance matrix created with shape: {a_to_b_matrix.shape}")
#     print(f"ℹ️ Total unique nodes: {len(all_nodes)}")
#
#     return a_to_b_matrix


import pandas as pd

def create_distance_matrices(input_json, large_number=1000000):
    edges = input_json["data"]["distance_matrix"]
    all_nodes = set()

    # First pass: collect all unique node names
    for entry in edges:
        edge = entry["edge"].strip("()").split(", ")
        source = edge[0].strip()
        target = edge[1].strip()
        all_nodes.add(source)
        all_nodes.add(target)

    # Initialize empty distance DataFrame
    sorted_nodes = sorted(all_nodes)
    df = pd.DataFrame(large_number, index=sorted_nodes, columns=sorted_nodes)

    # Fill in distances from edge list
    for entry in edges:
        edge = entry["edge"].strip("()").split(", ")
        source = edge[0].strip()
        target = edge[1].strip()
        distance = entry["distance"]
        df.at[source, target] = distance

    print(f"Distance matrix created with shape: {df.shape}")
    print(f"Total unique nodes: {len(all_nodes)}")
    kit_holders = sorted([n for n in sorted_nodes if len(n.split('.')) == 2 or n == '0.0'])
    gravity_racks = sorted([n for n in sorted_nodes if len(n.split('.')) == 3 or n == '0.0.0'])
    node_order = kit_holders + gravity_racks
    df = df.reindex(index=node_order, columns=node_order)

    return df
