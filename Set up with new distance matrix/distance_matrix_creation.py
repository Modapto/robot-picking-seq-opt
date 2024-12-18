import json
import pandas as pd

def create_distance_matrices_new(input_data, large_number=1000000):
    """
    Function to create a bidirectional distance matrix from the new JSON format.

    Parameters:
    - input_data: JSON file path (str) or a dictionary containing the input data.
    - large_number: Value to replace NaN entries in the matrix for non-existent connections.

    Returns:
    - a_to_b_matrix: DataFrame representing bidirectional distances between nodes in a bipartite graph.
    """

    # If input_data is a file path (str), load the JSON content
    if isinstance(input_data, str):
        with open(input_data, 'r') as f:
            input_data = json.load(f)
    elif isinstance(input_data, dict):
        input_data = input_data  # If it's already a dict (e.g., from Postman), use it directly
    else:
        raise ValueError("Input data should be either a valid file path or a dictionary.")

    # Extract the filtered distance matrix from the input data
    distance_matrix = input_data.get('0.0', [])

    # Dictionary to store bidirectional distances between nodes
    a_to_b_data = {}

    # Iterate through the filtered matrix to build the bidirectional distance dictionary
    for entry in distance_matrix:
        for kh_position, connections in entry.items():
            for connection in connections:
                node = connection['node']  # Get the container node
                distance = connection['distance']  # Get the distance

                # Add forward distance (kit holder -> gravity rack)
                if kh_position not in a_to_b_data:
                    a_to_b_data[kh_position] = {}
                a_to_b_data[kh_position][node] = distance

                # Add reverse distance (gravity rack -> kit holder)
                if node not in a_to_b_data:
                    a_to_b_data[node] = {}
                a_to_b_data[node][kh_position] = distance

    # Convert the dictionary to a DataFrame
    a_to_b_matrix = pd.DataFrame.from_dict(a_to_b_data, orient='index')

    # Fill NaN values with the large number (for non-existing connections)
    a_to_b_matrix = a_to_b_matrix.fillna(large_number).astype('int64')

    # Separate nodes into kit holders and gravity racks
    kit_holders = sorted([node for node in a_to_b_matrix.index if len(node.split('.')) == 2])
    gravity_racks = sorted([node for node in a_to_b_matrix.index if len(node.split('.')) == 3])

    # Combine the node order: first kit holders, then gravity racks
    node_order = kit_holders + gravity_racks

    # Reindex rows and columns based on the combined node order
    a_to_b_matrix = a_to_b_matrix.reindex(index=node_order, columns=node_order, fill_value=large_number)

    # Return the finalized bidirectional distance matrix
    return a_to_b_matrix

# Example Usage
with open("random_configuration_distance_matrix_with_e_constraint.json", "r") as f:
    random_distance_matrix = json.load(f)

# Create the bidirectional distance matrix
distance_matrix = create_distance_matrices_new(random_distance_matrix)

# Save the resulting matrix to a CSV for visualization or debugging
distance_matrix.to_csv("distance_matrix_bidirectional.csv", index=True)

print("Bidirectional distance matrix created and saved successfully.")
