import random
import functools

#Nearest Neighbor TSP
def nearest_tsp(G, start, end, set_1, set_2, large_value=1000000):
    visit = {node: False for node in G.nodes}
    tour = [start]
    visit[start] = True
    current = start

    print(f"set_1 (kit holders): {set_1}")
    print(f"set_2 (gravity racks and start/end node): {set_2}")

    neighbors = [node for node in set_2 if not visit[node] and G.has_edge(current, node) and G[current][node]['weight_a_to_b'] < large_value]
    # print(f"Initial neighbors from {current} to set_2: {neighbors}")
    next_node = min(neighbors, key=lambda node: G[current][node]['weight_a_to_b'], default=None)

    if next_node is None:
        raise ValueError("No valid initial move from the start node to a gravity rack position.")

    tour.append(next_node)
    visit[next_node] = True
    current = next_node
    # print(f"First move to {next_node}")

    #create a set of kit holder nodes and exclude gravity racks nodes to handle the end of the algorithm and the return to starting/end node
    kit_holders = {node for node in set_1 if len(node.split('.')) == 2}

    while len(tour) < len(set_1) + len(set_2):
        if current in set_2:
            neighbors = [node for node in set_1 if not visit[node] and G.has_edge(current, node) and G[current][node]['weight_a_to_b'] < large_value]
            # print(f"Neighbors from {current} in set_2 to set_1: {neighbors}")
            next_node = min(neighbors, key=lambda node: G[current][node]['weight_a_to_b'], default=None)
        else:
            neighbors = [node for node in set_2 if not visit[node] and G.has_edge(current, node) and G[current][node]['weight_b_to_a'] < large_value]
            # print(f"Neighbors from {current} in set_1 to set_2: {neighbors}")
            next_node = min(neighbors, key=lambda node: G[current][node]['weight_b_to_a'], default=None)

        if next_node is None:
            # print(f"No valid neighbors found from {current}. Ending tour early.")
            break

        tour.append(next_node)
        visit[next_node] = True
        current = next_node

        # print(f"Current: {current}, Next: {next_node}, Tour: {tour}")

        if all(visit[node] for node in kit_holders):
            # print(f"All nodes in set_1 have been visited. Preparing to return to {end}.")
            break

    if tour[-1] != end:
        tour.append(end)
        # print(f"Added end node {end} to complete the tour.")

    return tour

#Total Cost Calculation
def total_cost(G, tour):
    cost = 0
    time_details = []
    for i in range(len(tour) - 1):
        u, v = tour[i], tour[i + 1]
        if u in G and v in G[u]:
            if G.nodes[u]['bipartite'] == 0 and G.nodes[v]['bipartite'] == 1:
                cost += G[u][v]['weight_a_to_b']
                time_details.append({
                    "from": u,
                    "to": v,
                    "totalTime": G[u][v]['weight_a_to_b']
                })
            else:
                cost += G[u][v]['weight_b_to_a']
                time_details.append({
                    "from": u,
                    "to": v,
                    "totalTime": G[u][v]['weight_b_to_a']
                })
    return cost, time_details

# 2-Opt Optimization
def find_best_two_opt_move(tour, graph, set_1, set_2):
    """
    This function identifies the best 2-opt move by comparing the current and new tour costs.
    It handles missing edges gracefully.
    """
    best_move_cost = 0  # Start with no improvement
    best_tour = tour[:]  # Initialize with the original tour

    for first_index in range(0, len(tour) - 2):
        A = tour[first_index]
        B = tour[first_index + 1]

        for second_index in range(first_index + 2, len(tour) - 1):
            K = tour[second_index]
            L = tour[second_index + 1]

            # Safely get current costs for existing edges
            current_cost_AB = graph[A][B]['weight_a_to_b'] if graph.has_edge(A, B) else float('inf')
            current_cost_KL = graph[K][L]['weight_a_to_b'] if graph.has_edge(K, L) else float('inf')

            # Calculate current total cost for these edges
            current_cost = current_cost_AB + current_cost_KL

            # Safely get new costs for the swapped edges
            new_cost_AK = graph[A][K]['weight_a_to_b'] if graph.has_edge(A, K) else float('inf')
            new_cost_BL = graph[B][L]['weight_a_to_b'] if graph.has_edge(B, L) else float('inf')

            # Calculate new total cost after swapping edges
            new_cost = new_cost_AK + new_cost_BL

            # Check if new cost is lower
            move_cost = new_cost - current_cost

            # If the move is valid and improves the tour, update the best move
            if move_cost < best_move_cost and new_cost_AK < float('inf') and new_cost_BL < float('inf'):
                best_move_cost = move_cost
                best_tour = apply_two_opt_move(tour, first_index, second_index)

    return best_tour, best_move_cost

def apply_two_opt_move(tour, i, k):
    """
    This function applies the best 2-opt move by reversing the segment between two nodes.
    """
    new_tour = tour[:i + 1]  # Keep the part before the reversed segment
    new_tour += tour[i + 1:k + 1][::-1]  # Reverse the segment between i and k
    new_tour += tour[k + 1:]  # Keep the rest of the tour unchanged
    return new_tour


def opt2(tour, graph, set_1, set_2, start=None, end=None):
    """
    This is the main 2-opt function that iteratively improves the tour by applying 2-opt moves.
    """
    # If no tour is provided, generate it using nearest_tsp
    if tour is None and start is not None and end is not None:
        print("Generating initial tour using Nearest Neighbor TSP...")
        tour = nearest_tsp(graph, start, end, set_1, set_2)

    best_tour = tour
    best_cost = total_cost(graph, best_tour)[0]
    print(f"Initial tour cost: {best_cost}")

    improved = True
    while improved:
        improved = False

        # Find the best possible 2-opt move
        new_tour, move_cost = find_best_two_opt_move(best_tour, graph, set_1, set_2)

        if move_cost < 0:
            best_tour = new_tour
            best_cost += move_cost
            improved = True
            print(f"Improved tour found with cost: {best_cost}")
        else:
            print("No further improvement found.")

    print(f"Final optimized tour cost: {best_cost}")
    return best_tour

# Q-Learning Parameters
ALPHA = 0.1  # Learning rate
GAMMA = 0.95  # Discount factor
EPSILON = 0.1  # Exploration factor


def q_learning_tsp(G, start, end, set_1, set_2, large_value=1000000, episodes=1000):
    q_table = {node: {neighbor: 0 for neighbor in G.neighbors(node)} for node in G.nodes}

    for _ in range(episodes):
        current_node = start
        tour = [current_node]
        visit = {node: False for node in G.nodes}
        visit[start] = True

        while len(tour) < len(set_1) + len(set_2):
            # Filter neighbors based on the large_value criteria
            valid_neighbors = [n for n in G.neighbors(current_node)
                               if not visit[n] and
                               ((current_node in set_1 and n in set_2 and G[current_node][n][
                                   'weight_a_to_b'] < large_value) or
                                (current_node in set_2 and n in set_1 and G[current_node][n][
                                    'weight_b_to_a'] < large_value))]

            if not valid_neighbors:
                break

            if random.uniform(0, 1) < EPSILON:
                next_node = random.choice(valid_neighbors)
            else:
                next_node = max(((n, q_table[current_node][n]) for n in valid_neighbors), key=lambda x: x[1])[0]

            reward = get_reward(G, current_node, next_node, set_1, set_2, large_value)
            max_next_q = max(q_table[next_node].values(), default=0)
            q_table[current_node][next_node] = (1 - ALPHA) * q_table[current_node][next_node] + \
                                               ALPHA * (reward + GAMMA * max_next_q)

            current_node = next_node
            tour.append(next_node)
            visit[next_node] = True

            if current_node in set_2 and all(visit[node] for node in set_2):
                break

        tour.append(end)

    return best_q_tour(q_table, G, start, end, set_1, set_2, large_value)


def get_reward(G, current, next_node, set_1, set_2, large_value):
    if current in set_1 and next_node in set_2:
        weight = G[current][next_node]['weight_a_to_b']
        if weight >= large_value:
            return -float('inf')  # Discourage transitions with large weights
        return -weight
    elif current in set_2 and next_node in set_1:
        weight = G[current][next_node]['weight_b_to_a']
        if weight >= large_value:
            return -float('inf')  # Discourage transitions with large weights
        return -weight
    else:
        return -float('inf')  # Large negative reward for invalid transitions


def best_q_tour(q_table, G, start, end, set_1, set_2, large_value):
    tour = [start]
    current = start
    visit = {node: False for node in q_table}
    visit[start] = True

    while len(tour) < len(set_1) + len(set_2):
        valid_neighbors = [n for n in q_table[current]
                           if not visit[n] and
                           ((current in set_1 and n in set_2 and G[current][n]['weight_a_to_b'] < large_value) or
                            (current in set_2 and n in set_1 and G[current][n]['weight_b_to_a'] < large_value))]
        if not valid_neighbors:
            break
        next_node = max(((n, q_table[current][n]) for n in valid_neighbors), key=lambda x: x[1])[0]
        tour.append(next_node)
        visit[next_node] = True
        current = next_node

        if current in set_2 and all(visit[node] for node in set_2):
            break

    tour.append(end)
    return tour