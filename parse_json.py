# REPOSITORY NAME (c) by the University of Piraues, Greece.
#
# REPOSITORY NAME is licensed under a
# Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <http://creativecommons.org/licenses/by-nc-nd/3.0/>.

import json
import pandas as pd

def create_distance_matrices(input_data, large_number=1000000):
    """
    Function to create a distance matrix from a JSON input.

    Parameters:
    - input_data: JSON file path (str) or a dictionary containing the input data.
    - large_number: Value to replace NaN entries in the matrix for non-existent connections.

    Returns:
    - a_to_b_matrix: DataFrame representing distances between nodes in a bipartite graph.
    """

    # If input_data is a file path (str), load the JSON content
    if isinstance(input_data, str):
        with open(input_data, 'r') as f:
            input_data = json.load(f)
    elif isinstance(input_data, dict):
        input_data = input_data  # If it's already a dict (e.g., from Postman), use it directly
    else:
        raise ValueError("Input data should be either a valid file path or a dictionary.")

    # Extract the distance matrix from the input data
    distance_matrix = input_data['data']['distanceMatrix']

    # Dictionary to store parsed distances between nodes
    a_to_b_data = {}

    # Iterate over each entry in the distance matrix
    for entry in distance_matrix:
        # Extract the route (e.g., "(A, B)") and distance
        edge = entry.get('edge')
        if edge:
            # Parse the nodes from the edge string (e.g., "A" and "B" from "(A, B)")
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

    # Return the finalized distance matrix
    return a_to_b_matrix