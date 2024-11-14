import random
import uuid
from time import *

def generate_random_json_input(k=0.5):
    methods = ["exact"]
    gravity_rack_positions = [f"{row}.{level}.{comp}"
                              for row in range(1, 2)
                              for level in range(1, 2)
                              for comp in range(1, 5)]

    kit_holder_positions = [f"{holder}.{block}"
                            for holder in range(1, 2)
                            for block in range(1, 5)]

    distance_matrix = []

    # Define edges between gravity racks and kit holders with dropout based on k
    for pointA in gravity_rack_positions:
        for pointB in kit_holder_positions:
            if random.uniform(0, 1) < k:  # Apply dropout based on k threshold
                aToBDist = random.randint(10000, 12000)
                bToADist = random.randint(10000, 12000)

                # Add forward direction
                distance_matrix.append({
                    "edge": f"({pointA}, {pointB})",
                    "distance": aToBDist
                })

                # Add reverse direction
                distance_matrix.append({
                    "edge": f"({pointB}, {pointA})",
                    "distance": aToBDist  # or use bToADist if distances are asymmetric
                })

    # Handle the start node (0.0): connects only to gravity rack positions (not kit holders)
    for pointB in gravity_rack_positions:
            aToBDist = random.randint(5000, 7000)
            distance_matrix.append({
                "edge": f"(0.0, {pointB})",
                "distance": aToBDist
            })

    # Handle the 0.0.0 pseudonode: can only get edges from kit holders and connect back to 0.0 with cost = 1
    for pointB in kit_holder_positions:
            aToBDist = random.randint(5000, 7000)
            distance_matrix.append({
                "edge": f"({pointB}, 0.0.0)",
                "distance": aToBDist
            })

    # Add the edge from 0.0.0 to 0.0 with cost = 1 (no dropout for this final edge)
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
