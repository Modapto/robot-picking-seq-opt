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
            weight = G[u][v]['weight']
            cost += weight
            time_details.append({
                "from": u,
                "to": v,
                "totalTime": weight
            })
    return cost, time_details


# 2-Opt Optimization
def find_best_two_opt_move(tour, graph, set_1, set_2):
    """
    This function identifies the best 2-opt move by comparing the current and new tour costs
    while ensuring valid transitions between kit holders (set_1) and gravity racks (set_2).
    """
    best_move_cost = 0  # Start with no improvement
    best_tour = tour[:]  # Initialize with the original tour

    for first_index in range(0, len(tour) - 2):
        A = tour[first_index]
        B = tour[first_index + 1]
        print(f"Checking edges ({A}, {B})")

        for second_index in range(first_index + 2, len(tour) - 1):
            K = tour[second_index]
            L = tour[second_index + 1]
            print(f"Considering swap between ({A}, {B}) and ({K}, {L})")

            current_cost_AB = graph[A][B]['weight'] if graph.has_edge(A, B) else float('inf')
            current_cost_KL = graph[K][L]['weight'] if graph.has_edge(K, L) else float('inf')
            current_cost = current_cost_AB + current_cost_KL
            print(f"Current edge costs: AB = {current_cost_AB}, KL = {current_cost_KL}, Total = {current_cost}")

            new_cost_AK = graph[A][K]['weight'] if graph.has_edge(A, K) else float('inf')
            new_cost_BL = graph[B][L]['weight'] if graph.has_edge(B, L) else float('inf')
            new_cost = new_cost_AK + new_cost_BL
            print(f"New edge costs: AK = {new_cost_AK}, BL = {new_cost_BL}, Total = {new_cost}")

            move_cost = new_cost - current_cost
            print(f"Move cost: {move_cost}")

            if move_cost < 0 and new_cost_AK < float('inf') and new_cost_BL < float('inf'):
                print(f"Found better tour by swapping edges: ({A}, {B}) with ({K}, {L})")
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

# def opt2(tour, graph, set_1, set_2, start=None, end=None):
#     """
#     Improved 2-opt function with an iteration limit to ensure all possible improvements are explored.
#     """
#     if tour is None and start is not None and end is not None:
#         print("Generating initial tour using Nearest Neighbor TSP...")
#         tour = nearest_tsp(graph, start, end, set_1, set_2)
#
#     best_tour = tour
#     best_cost = total_cost(graph, best_tour)[0]
#     print(f"Initial tour cost: {best_cost}")
#
#     improved = True
#     iteration = 0
#     while improved and iteration < 1000:
#         improved = False
#         new_tour, move_cost = find_best_two_opt_move(best_tour, graph, set_1, set_2)
#
#         if move_cost < 0:
#             best_tour = new_tour
#             best_cost += move_cost
#             improved = True
#             print(f"Improved tour found with cost: {best_cost}")
#         iteration += 1
#
#     print(f"Final optimized tour cost: {best_cost}")
#     return best_tour

def opt2(tour, graph, set_1, set_2, start=None, end=None):
    """
    Improved 2-opt function with an iteration limit to ensure all possible improvements are explored.
    """
    if tour is None and start is not None and end is not None:
        print("Generating initial tour using Nearest Neighbor TSP...")
        tour = nearest_tsp(graph, start, end, set_1, set_2)

    best_tour = tour
    best_cost = total_cost(graph, best_tour)[0]  # Calculate initial cost based on nearest neighbor tour
    print(f"Initial tour cost: {best_cost}")

    improved = True
    iteration = 0

    # Loop to optimize the tour using 2-opt algorithm
    while improved and iteration < 5000:  # Setting a limit of 1000 iterations
        improved = False

        # Try to find a better tour by 2-opt
        new_tour, move_cost = find_best_two_opt_move(best_tour, graph, set_1, set_2)

        if move_cost < 0:  # If we find a better tour, update it
            best_tour = new_tour
            best_cost += move_cost  # Adjust the best cost with the improvement
            improved = True
            print(f"Improved tour found with cost: {best_cost}")
        iteration += 1

    # After the optimization is done, print and save the best tour and cost
    final_cost = total_cost(graph, best_tour)[0]  # Recalculate the total cost of the best tour
    print(f"Final optimized tour cost: {final_cost}")

    # Make sure we return the **best_tour** after 2-opt, not the original tour
    return best_tour, final_cost  # Ensure we're returning the optimized tour and cost





