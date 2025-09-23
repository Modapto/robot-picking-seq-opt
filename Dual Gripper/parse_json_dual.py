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
