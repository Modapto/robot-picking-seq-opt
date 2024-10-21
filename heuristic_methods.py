import pandas as pd
import networkx as nx

def nearest_tsp(G, start, end, set_1, set_2, large_value=1000000):
    visit = {node: False for node in G.nodes}
    tour = [start]
    visit[start] = True
    current = start

    print(f"set_1 (kit holders): {set_1}")
    print(f"set_2 (gravity racks and start/end node): {set_2}")

    while len(tour) < len(set_1) + len(set_2) - 1:  # Ensure we visit all nodes before adding the end node
        if current in set_2 and current != end:  # Ensure we don't move to `0.0.0` before all kit holders are visited
            neighbors = [node for node in set_1 if not visit[node] and G.has_edge(current, node) and G[current][node]['weight'] < large_value]
            next_node = min(neighbors, key=lambda node: G[current][node]['weight'], default=None)
        else:
            neighbors = [node for node in set_2 if not visit[node] and node != end and G.has_edge(current, node) and G[current][node]['weight'] < large_value]
            next_node = min(neighbors, key=lambda node: G[current][node]['weight'], default=None)

        if next_node is None:
            raise ValueError(f"No valid neighbors found from {current}. The tour may be incomplete.")

        tour.append(next_node)
        visit[next_node] = True
        current = next_node

        # Debugging information
        print(f"Added node: {next_node}, Tour so far: {tour}")

        # Check if all kit holders (set_1) have been visited, if yes, then allow visiting 0.0.0
        if all(visit[node] for node in set_1 if node != '0.0'):
            print("All kit holders visited. Preparing to visit 0.0.0.")
            break

    # After all kit holders are visited, add the end node (0.0.0)
    tour.append(end)

    # Add the return from 0.0.0 back to 0.0
    if G.has_edge(end, start):
        tour.append(start)  # Add the return leg to the start node
        print(f"Returning from {end} to {start}.")

    return tour

def total_cost(G, tour):
    cost = 0
    time_details = []
    for i in range(len(tour) - 1):
        u, v = tour[i], tour[i + 1]
        if u in G and v in G[u]:
            # print(f"Edge {u} -> {v}, Weight: {G[u][v]['weight']}")  # Debugging line
            cost += G[u][v]['weight']
            time_details.append({
                "from": u,
                "to": v,
                "totalTime": G[u][v]['weight']
            })
    # print(f"Total cost for tour {tour}: {cost}")  # Debugging line
    return cost, time_details


# 2-Opt Optimization
def find_best_two_opt_move(tour, graph, set_1, set_2):
    """
    This function identifies the best 2-opt move by comparing the current and new tour costs
    while ensuring valid transitions between kit holders (set_1) and gravity racks (set_2).
    """
    best_move_cost = 0  # Start with no improvement
    best_tour = tour[:]  # Initialize with the original tour

    for i in range(1, len(tour) - 2):
        for k in range(i + 1, len(tour) - 1):
            A, B = tour[i - 1], tour[i]
            C, D = tour[k], tour[k + 1]

            # Ensure the alternation between kit holders and gravity racks
            if not (A in set_1 and B in set_2 and C in set_1 and D in set_2):
                continue

            # Get the current cost of the existing edges
            current_cost_AB_CD = (
                graph[A][B]['weight'] if graph.has_edge(A, B) else float('inf')
            ) + (
                graph[C][D]['weight'] if graph.has_edge(C, D) else float('inf')
            )

            # Get the new cost for the swapped edges
            new_cost_AC_BD = (
                graph[A][C]['weight'] if graph.has_edge(A, C) else float('inf')
            ) + (
                graph[B][D]['weight'] if graph.has_edge(B, D) else float('inf')
            )

            # Check if the new cost is better
            if new_cost_AC_BD < current_cost_AB_CD:
                best_move_cost = new_cost_AC_BD - current_cost_AB_CD
                best_tour = apply_two_opt_move(tour, i, k)

    return best_tour, best_move_cost


def apply_two_opt_move(tour, i, k):
    """
    This function applies the best 2-opt move by reversing the segment between two nodes.
    """
    new_tour = tour[:i + 1]  # Keep the part before the reversed segment
    new_tour += tour[i + 1:k + 1][::-1]  # Reverse the segment between i and k
    new_tour += tour[k + 1:]  # Keep the rest of the tour unchanged
    return new_tour

def opt2(tour, graph, set_1, set_2, start=None, end=None, max_iters=1000):
    """
    Improved 2-opt function with an iteration limit to ensure all possible improvements are explored.
    """
    if tour is None and start is not None and end is not None:
        print("Generating initial tour using Nearest Neighbor TSP...")
        tour = nearest_tsp(graph, start, end, set_1, set_2)

    best_tour = tour
    best_cost = total_cost(graph, best_tour)[0]
    print(f"Initial tour cost: {best_cost}")

    improved = True
    iteration = 0
    while improved and iteration < max_iters:
        improved = False
        new_tour, move_cost = find_best_two_opt_move(best_tour, graph, set_1, set_2)

        if move_cost < 0:
            best_tour = new_tour
            best_cost += move_cost
            improved = True
            print(f"Improved tour found with cost: {best_cost}")
        iteration += 1

    print(f"Final optimized tour cost: {best_cost}")
    return best_tour

def opt2_with_random_restarts(tour, graph, set_1, set_2, restarts=10):
    """
    2-opt with random restarts to avoid local minima and potentially find better solutions.
    """
    best_overall_tour = tour
    best_overall_cost = total_cost(graph, tour)[0]

    for i in range(restarts):
        # Randomly shuffle the tour
        random.shuffle(tour)
        new_tour = opt2(tour, graph, set_1, set_2)

        # Compare the new tour cost
        new_cost = total_cost(graph, new_tour)[0]
        if new_cost < best_overall_cost:
            best_overall_tour = new_tour
            best_overall_cost = new_cost
            print(f"New best tour found with cost: {best_overall_cost} after restart {i+1}")

    return best_overall_tour


# # 2-Opt Optimization
# def find_best_two_opt_move(tour, graph, set_1, set_2):
#     best_move_cost = 0
#     best_tour = tour[:]
#
#     for first_index in range(0, len(tour) - 2):
#         A = tour[first_index]
#         B = tour[first_index + 1]
#         # print(f"Checking edges ({A}, {B})")
#
#         for second_index in range(first_index + 2, len(tour) - 1):
#             K = tour[second_index]
#             L = tour[second_index + 1]
#             # print(f"Considering swap between ({A}, {B}) and ({K}, {L})")
#
#             current_cost_AB = graph[A][B]['weight'] if graph.has_edge(A, B) else float('inf')
#             current_cost_KL = graph[K][L]['weight'] if graph.has_edge(K, L) else float('inf')
#             current_cost = current_cost_AB + current_cost_KL
#             # print(f"Current edge costs: AB = {current_cost_AB}, KL = {current_cost_KL}, Total = {current_cost}")
#
#             new_cost_AK = graph[A][K]['weight'] if graph.has_edge(A, K) else float('inf')
#             new_cost_BL = graph[B][L]['weight'] if graph.has_edge(B, L) else float('inf')
#             new_cost = new_cost_AK + new_cost_BL
#             # print(f"New edge costs: AK = {new_cost_AK}, BL = {new_cost_BL}, Total = {new_cost}")
#
#             move_cost = new_cost - current_cost
#             # print(f"Move cost: {move_cost}")
#
#             if move_cost < best_move_cost and new_cost_AK < float('inf') and new_cost_BL < float('inf'):
#                 # print(f"Found better tour by swapping edges: ({A}, {B}) with ({K}, {L})")
#                 best_move_cost = move_cost
#                 best_tour = apply_two_opt_move(tour, first_index, second_index)
#
#     return best_tour, best_move_cost
#
# def apply_two_opt_move(tour, i, k):
#     new_tour = tour[:i + 1]
#     new_tour += tour[i + 1:k + 1][::-1]
#     new_tour += tour[k + 1:]
#     # print(f"Applied 2-opt move between indices {i} and {k}")
#     return new_tour
#
# def opt2(tour, graph, set_1, set_2, start=None, end=None, max_iters=1000, tolerance=1e-6):
#     if tour is None and start is not None and end is not None:
#         print("Generating initial tour using Nearest Neighbor TSP...")
#         tour = nearest_tsp(graph, start, end, set_1, set_2)
#         print(f"Initial tour generated: {tour}")
#
#     if not tour:
#         print("Error: No valid initial tour generated.")
#         return None
#
#     best_tour = tour
#     best_cost = total_cost(graph, best_tour)[0]
#     print(f"Initial tour cost: {best_cost}")
#
#     improved = True
#     while improved:
#         improved = False
#         new_tour, move_cost = find_best_two_opt_move(best_tour, graph, set_1, set_2)
#
#         if move_cost < 0:
#             best_tour = new_tour
#             best_cost += move_cost  # Update cost incrementally
#             improved = True
#             # print(f"Improved tour found with cost: {best_cost}")
#         else:
#             print("No further improvement found.")
#
#     final_cost, _ = total_cost(graph, best_tour)
#     print(f"Final optimized tour cost: {final_cost}")
#     return best_tour





