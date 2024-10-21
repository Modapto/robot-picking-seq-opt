import random
import uuid
from time import *
import json

def generate_random_json_input():
    methods = ["2-opt"]
    # "nearest",, "q_learning", "exact", "2-opt"
    # # Gravity rack positions
    # gravity_rack_positions = [f"{row}.{level}.{comp}"
    #                           for row in range(1, 2)
    #                           for level in range(1, 2)
    #                           for comp in range(1, 3)]
    #
    # # Kit holder positions
    # kit_holder_positions = [f"{holder}.{block}"
    #                         for holder in range(1, 2)
    #                         for block in range(1, 3)]
    # # Increase Gravity rack positions
    # gravity_rack_positions = [f"{row}.{level}.{comp}"
    #                           for row in range(1, 5)
    #                           for level in range(1, 3)
    #                           for comp in range(1, 5)]
    #
    # # Increase Kit holder positions
    # kit_holder_positions = [f"{holder}.{block}"
    #                         for holder in range(1, 5)
    #                         for block in range(1, 3)]
    # # Gravity rack positions
    # gravity_rack_positions = [f"{row}.{level}.{comp}"
    #                           for row in range(1, 7)
    #                           for level in range(1, 3)
    #                           for comp in range(1, 9)]
    #
    # #Kit holder positions
    # kit_holder_positions = [f"{holder}.{block}"
    #                         for holder in range(1, 5)
    #                         for block in range(1, 7)]
    # 10 Gravity rack positions
    gravity_rack_positions = [f"{row}.{level}.{comp}"
                              for row in range(1, 2)
                              for level in range(1, 3)
                              for comp in range(1, 6)]  # 8 gravity rack nodes

    # 6 Kit holder positions
    kit_holder_positions = [f"{holder}.{block}"
                            for holder in range(1, 3)
                            for block in range(1, 3)]  # 4 kit holder nodes
    # Generate the new distance matrix format
    distance_matrix = []

    # Define edges between gravity racks and kit holders (bipartite graph)
    for pointA in gravity_rack_positions:
        for pointB in kit_holder_positions:
            aToBDist = random.randint(10000, 20000)
            bToADist = random.randint(10000, 20000)

            # Add forward direction
            distance_matrix.append({
                "edge": f"({pointA}, {pointB})",
                "distance": aToBDist
            })

            # Add reverse direction
            distance_matrix.append({
                "edge": f"({pointB}, {pointA})",
                "distance": bToADist
            })

    # Handle the start node (0.0): connects only to gravity rack positions (not kit holders)
    for pointB in gravity_rack_positions:
        aToBDist = random.randint(5000, 15000)

        # Add forward direction (from 0.0 to pointB, gravity racks only)
        distance_matrix.append({
            "edge": f"(0.0, {pointB})",
            "distance": aToBDist
        })

    # Handle the 0.0.0 pseudonode: can only get edges from kit holders and connect back to 0.0 with cost = 1
    for pointB in kit_holder_positions:
        aToBDist = random.randint(5000, 15000)

        # Add edge from kit holders to 0.0.0
        distance_matrix.append({
            "edge": f"({pointB}, 0.0.0)",
            "distance": aToBDist
        })

    # Add the edge from 0.0.0 to 0.0 with cost = 1
    distance_matrix.append({
        "edge": "(0.0.0, 0.0)",
        "distance": 1
    })

    random_json_input = {
        "route": "robot-pick-seq-opt",
        "uuid": str(uuid.uuid4()),
        "generated_at": int(time()),
        "data": {
            "method": random.choice(methods),
            "start_node": "0.0",
            "end_node": "0.0.0",
            "distanceMatrix": distance_matrix
        }
    }

    return random_json_input
