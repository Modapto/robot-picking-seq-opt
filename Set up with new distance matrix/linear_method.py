from distance_matrix_creation import *
from graph_creation import *
import json
import time
import numpy as np

# File path to the input JSON
json_file_path = "final_random_configuration.json"
# Start timing for the solution
solution_time_start = int(time.time() * 1000)
# Open and load the JSON file
try:
    with open(json_file_path, 'r') as f:
        input_data = json.load(f)
    print(f"Local JSON input has been loaded from {json_file_path}.")
except FileNotFoundError:
    print(f"Error: The file {json_file_path} does not exist.")
    exit(1)  # Exit the script if the file is missing

# Parse the distance matrices
a_to_b_matrix = create_distance_matrices(input_data)
print(a_to_b_matrix)
print("Distance matrices created!")

# Create the bipartite graph
B, set_1, set_2 = create_directed_bipartite_graph(a_to_b_matrix)
print("Graph generated!")

# Extract important fields from the input data
start_node = input_data['data'].get('start_node', '0.0')
end_node = input_data['data'].get('end_node', '0.0.0')
method = input_data['data'].get('method', 'linear_picking')

# Initialize result storage and timing
results = {}
# solution_time_start = int(time.time() * 1000)  # Start timing for solution
total_time_start = solution_time_start


def linear_picking(B, start_node, end_node, set_1, set_2):
    """
    Simulates the industrial workflow with a linear picking sequence.

    Parameters:
        B (networkx.DiGraph): The directed bipartite graph with distances between nodes.
        start_node (str): Starting node of the tour (e.g., "0.0").
        end_node (str): Ending node of the tour (e.g., "0.0.0").
        set_1 (list): List of kit holder positions.
        set_2 (list): List of gravity rack positions.

    Returns:
        dict: A linear picking sequence (tour) and total cost.
    """
    tour = [start_node]  # Start from the initial node
    total_cost = 0

    # Iterate over each position in set_1 sequentially
    for position in sorted(set_1):  # Ensure positions are processed in order
        matching_rack = None
        min_distance = float('inf')

        for rack in set_2:
            if B.has_edge(rack, position):  # Check if connection exists
                distance = B[rack][position]['weight']  # Access the edge weight
                if distance < min_distance:
                    min_distance = distance
                    matching_rack = rack

        if matching_rack:
            # Move from current node to the matching rack
            if B.has_edge(tour[-1], matching_rack):
                tour.append(matching_rack)
                total_cost += B[tour[-2]][matching_rack]['weight']

            # Move from rack to kit holder position
            tour.append(position)
            total_cost += min_distance

    # Return to the end node
    if tour[-1] != end_node:
        tour.append(end_node)
        if B.has_edge(tour[-2], end_node):
            total_cost += B[tour[-2]][end_node]['weight']

    return {"tour": tour, "total_cost": total_cost}


def total_cost(G, tour):
    """
    Function to calculate the total cost of a given tour.

    Calculate the total cost of a tour.

    Parameters:
    - G: A graph representing the problem.
    - tour: List of nodes representing the tour.

    Returns:
    - cost: Total cost of the tour.
    - time_details: List of details for each segment of the tour.
    """
    cost = 0
    time_details = []
    for i in range(len(tour) - 1):
        u, v = tour[i], tour[i + 1]
        if u in G and v in G[u]:
            weight = G[u][v]['weight']
            cost += weight
            time_details.append({
                "from": u,
                "to": v,
                "totalTime": weight
            })
    return cost, time_details



# Run the linear picking TSP
try:
    if method == "linear_picking" or method == "all":
        print("Running Linear Picking TSP...")
        linear_tour = linear_picking(B, start_node, end_node, set_1, set_2)

        if linear_tour:
            cost, time_details = total_cost(B, linear_tour['tour'])

            results["linear_picking"] = {
                "tour": linear_tour["tour"],
                "cost": cost,
                "time_details": time_details,
                "totalLoadingTime": cost
            }
            print(f"Linear Picking TSP completed. Cost: {cost}")

except ValueError as e:
    print(f"Error in linear picking method: {e}")

# End timing for the solution
end_time = int(time.time() * 1000)


# Function to convert data types for JSON serialization
def convert_to_native_types(data):
    if isinstance(data, dict):
        return {k: convert_to_native_types(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_to_native_types(v) for v in data]
    elif isinstance(data, np.integer):
        return int(data)
    else:
        return data

# Prepare picking sequence
picking_seq = []
total_loading_time = None
for method, result in results.items():
    if "time_details" in result:
        picking_seq.append({"method": method})
        picking_seq.extend(result["time_details"])
        total_loading_time = result["totalLoadingTime"]

# Prepare the output data
output_data = {
    "uuid": input_data['uuid'],
    "produced_at": int(time.time() * 1000),
    "data": {
        "pickingSeq": picking_seq,
        "totalLoadingTime": str(total_loading_time),
        "solutionTime": end_time - solution_time_start,
        "totalTime": end_time - total_time_start
    }
}
print(f"Solution start time: {solution_time_start}")
print(f"Solution end time: {end_time}")
print(f"Solution duration: {end_time - solution_time_start} ms")

output_data = convert_to_native_types(output_data)

# Save the output to a JSON file
output_json_file_path = "linear_method_result.json"
try:
    with open(output_json_file_path, 'w') as json_file:
        json.dump(output_data, json_file, indent=4)
    print(f"Local output saved to {output_json_file_path}")
except IOError as e:
    print(f"Error saving output JSON: {e}")
