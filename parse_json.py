import json
import pandas as pd

def create_distance_matrices(input_data, large_number=1000000):
    """
    Unified function to create distance matrices either from JSON input or already parsed data.

    Parameters:
    - input_data: Can be a JSON file path (str) or already loaded input data (dict).
    - large_number: Default large number to fill NaN values in the matrices.

    Returns:
    - a_to_b_matrix: DataFrame representing distances from set_1 to set_2.
    """

    # If input_data is a file path (str), load the JSON content
    if isinstance(input_data, str):
        with open(input_data, 'r') as f:
            input_data = json.load(f)
    elif isinstance(input_data, dict):
        # If it's already a dict (e.g., from Postman), use it directly
        input_data = input_data
    else:
        raise ValueError("Input data should be either a valid file path or a dictionary.")

    # Extract the distance matrix from the input data
    distance_matrix = input_data['data']['distanceMatrix']

    a_to_b_data = {}

    # Parse each entry in the distance matrix
    for entry in distance_matrix:
        # Parse route assuming it's formatted like "(A, B)"
        edge = entry.get('edge')
        if edge:
            pointA, pointB = edge.strip('()').split(', ')

            # Extract the distance
            distance = entry['distance']

            # Add the distances from pointA to pointB
            if pointB not in a_to_b_data:
                a_to_b_data[pointB] = {}
            a_to_b_data[pointB][pointA] = distance  # Reverse direction for distance matrix

    # Create a DataFrame for the distance matrix
    a_to_b_matrix = pd.DataFrame(a_to_b_data)

    # Fill NaN values with the large number (for non-existing connections)
    a_to_b_matrix = a_to_b_matrix.fillna(large_number).astype('int64')

    # Handle node ordering: treat 0.0 as a kit holder and 0.0.0 as a gravity rack
    kit_holders = sorted([node for node in a_to_b_matrix.index if len(node.split('.')) == 2 or node == '0.0'])
    gravity_racks = sorted([node for node in a_to_b_matrix.index if len(node.split('.')) == 3 or node == '0.0.0'])

    # Combine the node order: first kit holders, then gravity racks
    node_order = kit_holders + gravity_racks

    # Reindex rows and columns based on the combined node order
    a_to_b_matrix = a_to_b_matrix.reindex(index=node_order, columns=node_order, fill_value=large_number)

    return a_to_b_matrix