import json
import pandas as pd

def create_distance_matrices_from_json(json_file_path, large_number=1000000):
    with open(json_file_path, 'r') as f:
        input_data = json.load(f)

    #distance matrix
    distance_matrix = input_data['data']['distanceMatrix']

    a_to_b_data = {}
    b_to_a_data = {}

    for entry in distance_matrix:
        pointA = entry['pointA']
        pointB = entry['pointB']
        a_to_b_dist = entry['aToBDist']
        b_to_a_dist = entry['bToADist']

        if pointA not in a_to_b_data:
            a_to_b_data[pointA] = {}
        if pointB not in b_to_a_data:
            b_to_a_data[pointB] = {}

        a_to_b_data[pointA][pointB] = a_to_b_dist
        b_to_a_data[pointB][pointA] = b_to_a_dist

    a_to_b_matrix = pd.DataFrame(a_to_b_data)
    b_to_a_matrix = pd.DataFrame(b_to_a_data)

    #0.0.0 node included in both matrices
    if '0.0.0' not in a_to_b_matrix.columns:
        a_to_b_matrix['0.0.0'] = large_number
    if '0.0.0' not in b_to_a_matrix.index:
        b_to_a_matrix.loc['0.0.0'] = large_number

    # Fill NaN values with large_number and convert to integer
    a_to_b_matrix = a_to_b_matrix.fillna(large_number).astype(int)
    b_to_a_matrix = b_to_a_matrix.fillna(large_number).astype(int)

    return a_to_b_matrix, b_to_a_matrix

def create_distance_matrices_from_postman(input_postman_file_path, large_number=1000000):
    if isinstance(input_postman_file_path, str):
        with open(input_postman_file_path, 'r') as f:
            input_data = json.load(f)
    else:
        input_data = input_postman_file_path

    #distance matrix
    distance_matrix = input_data['data']['distanceMatrix']

    a_to_b_data = {}
    b_to_a_data = {}

    for entry in distance_matrix:
        pointA = entry['pointA']
        pointB = entry['pointB']
        a_to_b_dist = entry['aToBDist']
        b_to_a_dist = entry['bToADist']

        if pointA not in a_to_b_data:
            a_to_b_data[pointA] = {}
        if pointB not in b_to_a_data:
            b_to_a_data[pointB] = {}

        a_to_b_data[pointA][pointB] = a_to_b_dist
        b_to_a_data[pointB][pointA] = b_to_a_dist

    a_to_b_matrix = pd.DataFrame(a_to_b_data)
    b_to_a_matrix = pd.DataFrame(b_to_a_data)

    #0.0.0 node is included in both matrices
    if '0.0.0' not in a_to_b_matrix.columns:
        a_to_b_matrix['0.0.0'] = large_number
    if '0.0.0' not in b_to_a_matrix.index:
        b_to_a_matrix.loc['0.0.0'] = large_number

    #Fill NaN values with large_number and convert to integer
    a_to_b_matrix = a_to_b_matrix.fillna(large_number).astype(int)
    b_to_a_matrix = b_to_a_matrix.fillna(large_number).astype(int)

    return a_to_b_matrix, b_to_a_matrix
