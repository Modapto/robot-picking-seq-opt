import random
import uuid
from time import time
from GraphCreation import create_distance_matrices, create_directed_bipartite_graph
from heuristic_methods import nearest_tsp


def generate_random_json_input(gravity_rack_positions=None, kit_holder_positions=None, method="nearest", k=0.5):
    """
    Generate a random JSON input with a dropout rate controlled by k.
    """
    if gravity_rack_positions is None:
        gravity_rack_positions = [f"{row}.{level}.{comp}" for row in range(1, 7) for level in range(1, 3) for comp in
                                  range(1, 9)]
    if kit_holder_positions is None:
        kit_holder_positions = [f"{holder}.{block}" for holder in range(1, 5) for block in range(1, 7)]

    distance_matrix = []

    # Define edges between gravity racks and kit holders with dropout rate k
    for pointA in gravity_rack_positions:
        for pointB in kit_holder_positions:
            if random.uniform(0, 1) > k:  # Apply dropout rate k = 0.5
                aToBDist = random.randint(10000, 20000)
                distance_matrix.append({"edge": f"({pointA}, {pointB})", "distance": aToBDist})
                distance_matrix.append({"edge": f"({pointB}, {pointA})", "distance": aToBDist})

    # Ensure edges for start and pseudonode 0.0.0
    for pointB in gravity_rack_positions:
        distance_matrix.append({"edge": f"(0.0, {pointB})", "distance": random.randint(5000, 15000)})

    for pointB in kit_holder_positions:
        distance_matrix.append({"edge": f"({pointB}, 0.0.0)", "distance": random.randint(5000, 15000)})

    distance_matrix.append({"edge": "(0.0.0, 0.0)", "distance": 1})

    random_json_input = {
        "route": "robot-pick-seq-opt",
        "uuid": str(uuid.uuid4()),
        "generated_at": int(time()),
        "data": {
            "method": method,
            "start_node": "0.0",
            "end_node": "0.0.0",
            "distanceMatrix": distance_matrix
        }
    }

    return random_json_input


from reinforcement_learning import q_learning_tsp

def is_feasible(input_json):
    try:
        # Parse distance matrices and create the graph
        a_to_b_matrix = create_distance_matrices(input_json)
        B, set_1, set_2 = create_directed_bipartite_graph(a_to_b_matrix)

        # Retrieve start and end nodes
        start_node = input_json['data'].get('start_node', '0.0')
        end_node = input_json['data'].get('end_node', '0.0.0')

        # Check feasibility using Nearest Neighbor
        try:
            nearest_tour = nearest_tsp(B, start_node, end_node, set_1, set_2)
            print("Nearest Neighbor method found a feasible solution.")
        except ValueError as e:
            print(f"Infeasible instance detected in nearest neighbor check: {e}")
            return False

        # Check feasibility using Q-Learning
        try:
            q_learning_tour = q_learning_tsp(B, start_node, end_node, set_1, set_2, episodes=1500)

            # Validate that Q-learning visits all kit holder nodes
            visited_nodes = set(q_learning_tour)
            unvisited_kit_holders = [node for node in set_1 if node != start_node and node not in visited_nodes]

            if unvisited_kit_holders:
                print(f"Infeasible instance detected in Q-learning: Unvisited kit holder nodes: {unvisited_kit_holders}")
                return False
            print("Q-Learning method found a feasible solution.")
        except Exception as e:
            print(f"Infeasible instance detected in Q-learning check: {e}")
            return False

        # If both checks pass, the instance is feasible
        return True
    except Exception as e:
        print(f"Error during feasibility check: {e}")
        return False



def generate_feasible_instance(gravity_rack_positions, kit_holder_positions, k=0.5):
    while True:
        input_json = generate_random_json_input(gravity_rack_positions, kit_holder_positions, method="all")
        if is_feasible(input_json):
            print("Feasible instance generated!")
            return input_json
        print("Infeasible instance generated. Retrying...")



