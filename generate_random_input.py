import random
import uuid
from time import *

def generate_random_json_input():
    methods = ["exact"]
    # , "q-learning", "exact", "nearest", "2-opt"
    # Dummy - Baby Example
    # #Gravity rack positions
    # gravity_rack_positions = [f"{row}.{level}.{comp}"
    #                           for row in range(1, 2)
    #                           for level in range(1, 2)
    #                           for comp in range(1, 3)]
    #
    # #Kit holder positions
    # kit_holder_positions = [f"{holder}.{block}"
    #                         for holder in range(1, 2)
    #                         for block in range(1, 3)]
    #Gravity rack positions
    # gravity_rack_positions = [f"{row}.{level}.{comp}"
    #                           for row in range(1, 7)
    #                           for level in range(1, 3)
    #                           for comp in range(1, 9)]
    #
    # #Kit holder positions
    # kit_holder_positions = [f"{holder}.{block}"
    #                         for holder in range(1, 5)
    #                         for block in range(1, 7)]

    # gravity_rack_positions = [f"{row}.{level}.{comp}"
    #                           for row in range(1, 11)
    #                           for level in range(1, 3)
    #                           for comp in range(1, 11)]
    #
    # # Kit holder positions
    # kit_holder_positions = [f"{holder}.{block}"
    #                         for holder in range(1, 5)
    #                         for block in range(1, 6)]

    gravity_rack_positions = [f"{row}.{level}.{comp}"
                              for row in range(1, 3)
                              for level in range(1, 3)
                              for comp in range(1, 11)]

    #Kit holder positions
    kit_holder_positions = [f"{holder}.{block}"
                            for holder in range(1, 5)
                            for block in range(1, 6)]

    #Generate distance matrix with random distances
    distance_matrix = []
    for pointA in gravity_rack_positions:
        for pointB in kit_holder_positions:
            aToBDist = random.randint(1000, 2000)
            bToADist = random.randint(1000, 2000)
            distance_matrix.append({
                "pointA": pointA,
                "pointB": pointB,
                "aToBDist": aToBDist,
                "bToADist": bToADist
            })

    for pointA in ["0.0.0"]:
        for pointB in gravity_rack_positions[:]:  #Exclude the start node itself
            aToBDist = random.randint(500, 1500)
            bToADist = random.randint(500, 1500)
            distance_matrix.append({
                "pointA": pointA,
                "pointB": pointB,
                "aToBDist": aToBDist,
                "bToADist": bToADist
            })

    for pointA in ["0.0.0"]:
        for pointB in kit_holder_positions[:]:  #Exclude the start node itself
            aToBDist = random.randint(500, 1500)
            bToADist = random.randint(500, 1500)
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
            "method": random.choice(methods),
            "start_node": "0.0.0",
            "end_node": "0.0.0",
            "distanceMatrix": distance_matrix
        }
    }

    return random_json_input