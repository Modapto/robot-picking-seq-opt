import random
import uuid
from time import *
import json

# Function to generate a random JSON input for the bipartite TSP problem
def generate_random_json_input():
    # Define possible methods for solving the TSP problem
    methods = ["exact", "nearest", "2-opt", "q_learning", "ql-nearest", "ql-2-opt"]

    # Gravity rack positions in the format "row.level.component"
    gravity_rack_positions = [f"{row}.{level}.{comp}"
                              for row in range(1, 2)
                              for level in range(1, 2)
                              for comp in range(1, 11)]

    # Kit holder positions in the format "holder.block"
    kit_holder_positions = [f"{holder}.{block}"
                            for holder in range(1, 2)
                            for block in range(1, 11)]

    # Generate the new distance matrix format
    distance_matrix = []

    # Define edges between gravity racks and kit holders (bipartite graph)
    for pointA in gravity_rack_positions:
        for pointB in kit_holder_positions:
            aToBDist = random.randint(10000, 12000)
            bToADist = random.randint(10000, 12000)

            # Add forward direction (gravity rack to kit holder)
            distance_matrix.append({
                "edge": f"({pointA}, {pointB})",
                "distance": aToBDist
            })

            # Add reverse direction (kit holder to gravity rack)
            distance_matrix.append({
                "edge": f"({pointB}, {pointA})",
                "distance": aToBDist
            })

    # Handle the start node (0.0): connects only to gravity rack positions (not kit holders)
    for pointB in gravity_rack_positions:
        aToBDist = random.randint(5000, 7000)

        # Add forward direction (from 0.0 to pointB, gravity racks only)
        distance_matrix.append({
            "edge": f"(0.0, {pointB})",
            "distance": aToBDist
        })

    # Handle the 0.0.0 pseudonode: can only get edges from kit holders and connect back to 0.0 with cost = 1
    for pointB in kit_holder_positions:
        aToBDist = random.randint(5000, 7000)

        # Add edge from kit holders to 0.0.0
        distance_matrix.append({
            "edge": f"({pointB}, 0.0.0)",
            "distance": aToBDist
        })

    # Add the edge from 0.0.0 to 0.0 with cost = 1
    distance_matrix.append({
        "edge": "(0.0.0, 0.0)",
        "distance": 0
    })

    # Create the JSON structure for the input
    random_json_input = {
        "route": "robot-pick-seq-opt",
        "uuid": str(uuid.uuid4()),  # Generate a unique identifier for the input
        "generated_at": int(time()),  # Timestamp of when the input was generated
        "data": {
            "method": random.choice(methods),
            "start_node": "0.0",
            "end_node": "0.0.0",
            "distanceMatrix": distance_matrix
        }
    }

    # Return the generated JSON input
    return random_json_input
