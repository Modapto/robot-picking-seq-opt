import random
import pandas as pd

def ql_nearest_tsp(G, start, end, set_1, set_2, large_value=1000000, q_values_file='q_values.csv'):
    """
    Function to implement Q-learning combined with the nearest neighbor heuristic.

    Solve the TSP using Q-learning Q-values combined with a nearest neighbor approach.

    Parameters:
    - G: Graph representing the problem.
    - start: Start node ('0.0').
    - end: End node ('0.0.0').
    - set_1: List of kit holder nodes.
    - set_2: List of gravity rack nodes.
    - large_value: Large value representing invalid connections.
    - q_values_file: Path to the CSV file containing pre-trained Q-values.

    Returns:
    - tour: List of nodes representing the computed tour.
    """
    # Load Q-values from the CSV file
    q_df = pd.read_csv(q_values_file, index_col=0)

    visit = {node: False for node in G.nodes}
    tour = [start]
    visit[start] = True
    current = start

    while len(tour) < len(set_1) + len(set_2) - 1:  # Ensure we visit all nodes before adding the end node
        # Alternate between set_1 and set_2 nodes as before
        if current in set_2 and current != end:
            neighbors = [node for node in set_1 if
                         not visit[node] and G.has_edge(current, node) and G[current][node]['weight'] < large_value]
        else:
            neighbors = [node for node in set_2 if
                         not visit[node] and node != end and G.has_edge(current, node) and G[current][node][
                             'weight'] < large_value]

        # Find the neighbor with the highest Q-value for the next step
        next_node = max(neighbors, key=lambda node: q_df.loc[current, str(node)], default=None) if neighbors else None

        if next_node is None:
            raise ValueError(f"No valid neighbors found from {current}. The tour may be incomplete.")

        # Append the next node to the tour and mark it as visited
        tour.append(next_node)
        visit[next_node] = True
        current = next_node

        # Print the node added to the tour along with its actual distance from the distance matrix in G
        actual_distance = G[tour[-2]][next_node]['weight'] if tour[-2] in G and next_node in G[tour[-2]] else None
        print(f"Added node: {next_node}, Distance: {actual_distance}, Tour so far: {tour}")

        # Check if all kit holders (set_1) have been visited, and prepare to end tour
        if all(visit[node] for node in set_1 if node != '0.0'):
            print("All kit holders visited. Preparing to visit 0.0.0.")
            break

    # After all kit holders are visited, add the end node (0.0.0)
    tour.append(end)

    # Add the return from 0.0.0 back to the start
    if G.has_edge(end, start):
        tour.append(start)
        print(f"Returning from {end} to {start}.")

    return tour


def total_cost(G, tour):
    """
    Function to calculate the total cost of a tour.

    Calculate the total cost of a tour.

    Parameters:
    - G: Graph representing the problem.
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

def load_q_values(q_values_file):
    """
    Function to load Q-values from a CSV file
    """
    q_df = pd.read_csv(q_values_file, index_col=0)
    return q_df

def ql_FindBestTwoOptMoveForBipartite(top, tour, G, set_1, set_2, q_df, start_node='0.0'):
    """
    Function to find the best 2-opt move using Q-values.

    Find the best 2-opt move for a bipartite TSP using Q-values.

    Parameters:
    - top: Dictionary to store the best move details.
    - tour: Current tour as a list of nodes.
    - G: Graph representing the problem.
    - set_1: List of kit holder nodes.
    - set_2: List of gravity rack nodes.
    - q_df: DataFrame of Q-values.
    - start_node: The start node ('0.0').

    Updates:
    - top: Updates the best move details if a better move is found.
    """
    number_of_neighboring_solutions = 0

    for firstIndex in range(0, len(tour) - 2):
        A = tour[firstIndex]
        B = tour[firstIndex + 1]

        for secondIndex in range(firstIndex + 2, len(tour) - 1):
            K = tour[secondIndex]
            L = tour[secondIndex + 1]

            if (A in set_1 and K in set_2) or (A in set_2 and K in set_1) or A == start_node:
                number_of_neighboring_solutions += 1

                if A in q_df.index and K in q_df.columns and B in q_df.index and L in q_df.columns:
                    costAdded = q_df.loc[A, str(K)] + q_df.loc[B, str(L)]
                    costRemoved = q_df.loc[A, str(B)] + q_df.loc[K, str(L)]

                    moveCost = costAdded - costRemoved

                    if moveCost < top['moveCost']:
                        top['moveCost'] = moveCost
                        top['positionOfFirst'] = firstIndex
                        top['positionOfSecond'] = secondIndex
                else:
                    print(f"Q-value missing for transition: {A}->{K} or {B}->{L}")
    if start_node in tour:
        print(f"Swaps including the start node {start_node} are considered.")

def ql_ApplyTwoOptMoveForBipartite(top, tour):
    """
    Function to apply the best 2-opt move to the tour.

    Apply the best 2-opt move to the tour.

    Parameters:
    - top: Dictionary containing details of the best 2-opt move.
    - tour: Current tour as a list of nodes.

    Modifies:
    - tour: Updates the tour with the 2-opt move.
    """

    modifiedSequence = []

    # Add nodes before the first edge in reverse order
    i = 0
    while i <= top['positionOfFirst']:
        modifiedSequence.append(tour[i])
        i += 1

    # Reverse the nodes between the two edges
    i = top['positionOfSecond']
    while i > top['positionOfFirst']:
        modifiedSequence.append(tour[i])
        i -= 1

    # Add nodes after the second edge
    i = top['positionOfSecond'] + 1
    while i < len(tour):
        modifiedSequence.append(tour[i])
        i += 1

    # Update the tour with the new sequence
    for idx in range(len(tour)):
        tour[idx] = modifiedSequence[idx]  # Update original tour list with modified one

class ql_TwoOptMove:
    def __init__(self):
        self.positionOfFirst = None
        self.positionOfSecond = None
        self.moveCost = float('inf')  # Initialize with a high value to minimize

    def Initialize(self):
        self.positionOfFirst = None
        self.positionOfSecond = None
        self.moveCost = float('inf')  # Reset the move cost to infinity before each iteration


def ql_two_opt_for_bipartite(tour, G, set_1, set_2, q_values_file='q_values.csv', max_iterations=10000):
    """
    Function to perform 2-opt meta-heuristic optimization with Q-values.

    Perform 2-opt meta-heuristic optimization using Q-values.

    Parameters:
    - tour: Initial tour as a list of nodes.
    - G: Graph representing the problem.
    - set_1: List of kit holder nodes.
    - set_2: List of gravity rack nodes.
    - q_values_file: Path to the CSV file containing Q-values.
    - max_iterations: Maximum number of iterations.

    Returns:
    - best_tour: Optimized tour.
    - best_cost: Cost of the optimized tour.
    """
    # Load Q-values from CSV
    q_df = pd.read_csv(q_values_file, index_col=0)
    print("Q-values loaded from CSV:")
    print(q_df)

    best_tour = tour[:]
    best_cost, _ = total_cost(G, best_tour)  # Calculate cost with actual distances
    print(f"Initial Tour: {best_tour}, Initial Cost: {best_cost}")

    iteration = 0
    improved = True

    while improved and iteration < max_iterations:
        improved = False
        top = {'positionOfFirst': None, 'positionOfSecond': None, 'moveCost': float('inf')}

        for firstIndex in range(0, len(best_tour) - 2):
            A = best_tour[firstIndex]
            B = best_tour[firstIndex + 1]

            for secondIndex in range(firstIndex + 2, len(best_tour) - 1):
                K = best_tour[secondIndex]
                L = best_tour[secondIndex + 1]

                # Skip special pseudonodes
                if A in ['0.0', '0.0.0'] or B in ['0.0', '0.0.0'] or K in ['0.0', '0.0.0'] or L in ['0.0', '0.0.0']:
                    continue

                # Ensure nodes are connected in the graph
                try:
                    costAdded = q_df.loc[A, str(K)] + q_df.loc[B, str(L)]
                    costRemoved = q_df.loc[A, str(B)] + q_df.loc[K, str(L)]
                    moveCost = costAdded - costRemoved

                    actual_cost_added = G[A][K]['weight'] + G[B][L]['weight']
                    actual_cost_removed = G[A][B]['weight'] + G[K][L]['weight']
                    actual_move_cost = actual_cost_added - actual_cost_removed

                    if actual_move_cost < moveCost:
                        moveCost = actual_move_cost

                    if moveCost < top['moveCost']:
                        top['moveCost'] = moveCost
                        top['positionOfFirst'] = firstIndex
                        top['positionOfSecond'] = secondIndex
                except KeyError as e:
                    print(f"Skipping invalid edge: {e}")
                    continue

        if top['positionOfFirst'] is not None and top['moveCost'] < 0:
            ql_ApplyTwoOptMoveForBipartite(top, best_tour)
            improved = True
            best_cost, _ = total_cost(G, best_tour)
            print(f"Iteration {iteration + 1}: Updated Tour: {best_tour}, Total Cost: {best_cost}")
        else:
            print("No further improvement possible.")
            break

        iteration += 1

    print(f"2-opt terminated after {iteration} iterations.")
    print(f"Final Tour: {best_tour}, Final Cost: {best_cost}")
    return best_tour, best_cost

def validate_tour(tour, set_1, set_2):
    for i in range(len(tour) - 1):
        if tour[i] in set_1 and tour[i + 1] not in set_2:
            print(f"Invalid transition: {tour[i]} -> {tour[i + 1]}")
        if tour[i] in set_2 and tour[i + 1] not in set_1:
            print(f"Invalid transition: {tour[i]} -> {tour[i + 1]}")
