import json
import pandas as pd

def create_distance_matrices_new(input_data, large_number=1000000):

    if isinstance(input_data, str):
        with open(input_data, 'r') as f:
            input_data = json.load(f)
    elif isinstance(input_data, dict):
        input_data = input_data
    else:
        raise ValueError("Input data should be either a valid file path or a dictionary.")

    a_to_b_data = {}

    for source, connections in input_data.items():
        if not isinstance(connections, list):
            continue  # Ensure connections are a list
        for connection in connections:
            target = connection.get('node')
            distance = connection.get('distance')

            if target is None or distance is None:
                continue  # Skip invalid connections

            # Add source to target only if the source is explicitly connected to the target in the JSON
            if source not in a_to_b_data:
                a_to_b_data[source] = {}
            a_to_b_data[source][target] = distance

    a_to_b_matrix = pd.DataFrame.from_dict(a_to_b_data, orient='index')

    # Fill missing values with a large number and ensure distances are integers
    a_to_b_matrix = a_to_b_matrix.fillna(large_number).astype('int64')

    # Define node types
    kit_holders = sorted([node for node in a_to_b_matrix.index if len(node.split('.')) == 2])
    gravity_racks = sorted([node for node in a_to_b_matrix.index if len(node.split('.')) == 3])
    special_nodes = sorted([node for node in a_to_b_matrix.index if node in ["0.0", "0.0.0"]])

    # Order nodes: special nodes first, then kit holders, then gravity racks
    node_order = special_nodes + kit_holders + gravity_racks

    # Reindex matrix to match node order
    a_to_b_matrix = a_to_b_matrix.reindex(index=node_order, columns=node_order, fill_value=large_number)

    return a_to_b_matrix

# Load input JSON file
with open("configurations_with_extra_distance.json", "r") as f:
    random_distance_matrix = json.load(f)

# Create the bidirectional distance matrix
distance_matrix = create_distance_matrices_new(random_distance_matrix)

# Save the resulting matrix to a CSV for visualization or debugging
distance_matrix.to_csv("distance_matrix_creation.csv", index=True)

print("Bidirectional distance matrix created and saved successfully.")

