import random
import uuid
from time import *

def generate_random_json_input(gravity_rack_positions=None, kit_holder_positions=None, method="nearest"):
    # Set default positions if not provided
    if gravity_rack_positions is None:
        gravity_rack_positions = [f"{row}.{level}.{comp}"
                                  for row in range(1, 7)
                                  for level in range(1, 3)
                                  for comp in range(1, 9)]

    if kit_holder_positions is None:
        kit_holder_positions = [f"{holder}.{block}"
                                for holder in range(1, 5)
                                for block in range(1, 7)]

    #Generate distance matrix with random distances
    distance_matrix = []
    for pointA in gravity_rack_positions:
        for pointB in kit_holder_positions:
            aToBDist = random.randint(10000, 20000)
            bToADist = random.randint(10000, 20000)
            distance_matrix.append({
                "pointA": pointA,
                "pointB": pointB,
                "aToBDist": aToBDist,
                "bToADist": bToADist
            })

    for pointA in ["0.0.0"]:
        for pointB in gravity_rack_positions[:]:  #Exclude the start node itself
            aToBDist = random.randint(5000, 15000)
            bToADist = random.randint(5000, 15000)
            distance_matrix.append({
                "pointA": pointA,
                "pointB": pointB,
                "aToBDist": aToBDist,
                "bToADist": bToADist
            })

    for pointA in ["0.0.0"]:
        for pointB in kit_holder_positions[:]:  #Exclude the start node itself
            aToBDist = random.randint(5000, 15000)
            bToADist = random.randint(5000, 15000)
            distance_matrix.append({
                "pointA": pointA,
                "pointB": pointB,
                "aToBDist": aToBDist,
                "bToADist": bToADist
            })

    random_json_input = {
        "route": "robot-pick-seq-opt",
        "uuid": str(uuid.uuid4()),
        "generated_at": int(time()),
        "data": {
            "method": method,
            "start_node": "0.0.0",
            "end_node": "0.0.0",
            "distanceMatrix": distance_matrix
        }
    }

    return random_json_input