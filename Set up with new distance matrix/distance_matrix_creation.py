import json
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


def create_distance_matrices_from_json(json_file_path, large_number=1000000):
    """
    Creates a distance matrix from a JSON file containing distances between nodes.

    Parameters:
    - json_file_path: Path to the JSON file.
    - large_number: A large number to use as a placeholder for missing connections.

    Returns:
    - a_to_b_matrix: A pandas DataFrame representing the distance matrix.
    """
    with open(json_file_path, 'r') as f:
        data = json.load(f)

    # Prepare a dictionary to collect distances
    distances = {}

    for source, targets in data.items():
        for target_info in targets:
            target = target_info['node']
            distance = target_info['distance']

            if source not in distances:
                distances[source] = {}
            distances[source][target] = distance

    # Convert to a DataFrame and fill missing values
    a_to_b_matrix = pd.DataFrame(distances).fillna(large_number).astype(int)

    return a_to_b_matrix

# Load distance matrix and create the graph
json_file_path = 'configurations_with_extra_distance.json'
distance_matrix = create_distance_matrices_from_json(json_file_path)

