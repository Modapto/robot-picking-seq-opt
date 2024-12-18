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

    distance_matrix = input_data.get('0.0', [])

    a_to_b_data = {}

    for entry in distance_matrix:
        for kh_position, connections in entry.items():
            for connection in connections:
                node = connection['node']
                distance = connection['distance']

                # kit holder -> gravity rack
                if kh_position not in a_to_b_data:
                    a_to_b_data[kh_position] = {}
                a_to_b_data[kh_position][node] = distance

                # gravity rack -> kit holder
                if node not in a_to_b_data:
                    a_to_b_data[node] = {}
                a_to_b_data[node][kh_position] = distance

    a_to_b_matrix = pd.DataFrame.from_dict(a_to_b_data, orient='index')

    a_to_b_matrix = a_to_b_matrix.fillna(large_number).astype('int64')

    kit_holders = sorted([node for node in a_to_b_matrix.index if len(node.split('.')) == 2])
    gravity_racks = sorted([node for node in a_to_b_matrix.index if len(node.split('.')) == 3])

    node_order = kit_holders + gravity_racks

    a_to_b_matrix = a_to_b_matrix.reindex(index=node_order, columns=node_order, fill_value=large_number)

    return a_to_b_matrix

with open("random_configuration_distance_matrix_with_extra_distance.json", "r") as f:
    random_distance_matrix = json.load(f)

# Create the bidirectional distance matrix
distance_matrix = create_distance_matrices_new(random_distance_matrix)

# Save the resulting matrix to a CSV for visualization or debugging
distance_matrix.to_csv("distance_matrix_bidirectional.csv", index=True)

print("Bidirectional distance matrix created and saved successfully.")
