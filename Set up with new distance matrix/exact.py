import json
import pulp
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from distance_matrix_creation import create_distance_matrices

def classify_nodes(a_to_b_matrix):
    """
    Classify nodes into set_1 (kit holders) and set_2 (gravity racks), excluding special nodes.

    Parameters:
    - a_to_b_matrix: DataFrame containing the distance matrix.

    Returns:
    - set_1: List of kit holders.
    - set_2: List of gravity racks.
    """
    set_1 = [node for node in a_to_b_matrix.index if len(node.split('.')) == 2 and node != '0.0']  # Kit holders, exclude '0.0'
    set_2 = [node for node in a_to_b_matrix.index if len(node.split('.')) == 3 and node != '0.0.0']  # Gravity racks, exclude '0.0.0'
    return set_1, set_2


def create_distances_dict(a_to_b_matrix, set_1, set_2):
    """
    Function to create a distances dictionary from the matrix.

    Create a dictionary of distances from the distance matrix.

    Parameters:
    - a_to_b_matrix: DataFrame containing distances.
    - set_1: List of kit holders.
    - set_2: List of gravity racks.

    Returns:
    - distances: Dictionary mapping node pairs to distances.
    """
    distances = {}

    # Add connections between kit holders (set_1) and gravity racks (set_2)
    for point_a in set_1:
        for point_b in set_2:
            dist_a_to_b = a_to_b_matrix.at[point_a, point_b]
            dist_b_to_a = a_to_b_matrix.at[point_b, point_a]

            # Allow connections from kit holders (set_1) to '0.0.0'
            if point_b == '0.0.0':
                distances[(point_a, point_b)] = dist_a_to_b
                continue

            # Ensure the move from '0.0.0' to '0.0' is included with a valid distance
            if point_a == '0.0.0' and point_b == '0.0':
                distances[(
                point_a, point_b)] = dist_a_to_b if dist_a_to_b != 0 else 1  # Default distance is 1 if not provided
                continue

            # Allow connections from '0.0' to gravity racks
            if point_a == '0.0' and point_b in set_2:
                distances[(point_a, point_b)] = dist_a_to_b
                continue

            # Allow connections from kit holders to gravity racks (set_2)
            if point_a in set_1 and point_b in set_2 and dist_a_to_b != 0:
                distances[(point_a, point_b)] = dist_a_to_b
                distances[(point_b, point_a)] = dist_b_to_a
                continue

    # Add connections from '0.0' to all gravity racks (set_2)
    for point_b in set_2:
        dist_0_to_b = a_to_b_matrix.at['0.0', point_b]
        if dist_0_to_b != 0:  # Make sure the distance is non-zero
            distances[('0.0', point_b)] = dist_0_to_b

    # Add connections from all kit holders (set_1) to '0.0.0'
    for point_a in set_1:
        dist_a_to_0_0_0 = a_to_b_matrix.at[point_a, '0.0.0']
        if dist_a_to_0_0_0 != 0:  # Make sure the distance is non-zero
            distances[(point_a, '0.0.0')] = dist_a_to_0_0_0

    # Ensure '0.0.0' to '0.0' is always present with a distance of 1
    if ('0.0.0', '0.0') not in distances:
        distances[('0.0.0', '0.0')] = 1
    if ('0.0', '0.0.0') in distances:
        del distances['0.0', '0.0.0']  # Ensure no direct return from '0.0' to '0.0.0'

    return distances

def extract_possible_edges(distances):
    """
    Function to extract all possible edges from the distances dictionary.

    Extract all possible edges from the distances dictionary.

    Parameters:
    - distances: Dictionary of node pairs and distances.

    Returns:
    - List of possible edges.
    """
    possible_edges = [(i, j) for (i, j) in distances.keys()]

    # Remove the edge from '0.0' to '0.0.0', if present
    if ('0.0', '0.0.0') in possible_edges:
        possible_edges.remove(('0.0', '0.0.0'))

    # Ensure the final move from '0.0.0' to '0.0' is present
    if ('0.0.0', '0.0') not in possible_edges:
        possible_edges.append(('0.0.0', '0.0'))

    return possible_edges

def check_connectivity(SetA, SetB, distances):
    """
    Function to check the connectivity of the sets.

    Check if every node in Set A and Set B has at least one connection.

    Parameters:
    - SetA: List of nodes in set A.
    - SetB: List of nodes in set B.
    - distances: Dictionary of distances.
    """
    for a in SetA:
        if all((a, b) not in distances for b in SetB):
            print(f"No connections from {a} in Set A to any node in Set B")
    for b in SetB:
        if all((a, b) not in distances for a in SetA):
            print(f"No connections from {b} in Set B to any node in Set A")

def analyze_sets(set_a, set_b, distances):
    print("-------------------------------------------------------------------")
    print("Set A:", set_a)
    print("Number of nodes in Set A:", len(set_a))
    print("Set B:", set_b)
    print("Number of nodes in Set B:", len(set_b))

    # Check if the sizes match
    if len(set_a) != len(set_b):
        print("Warning: Set A and Set B do not contain the same number of nodes.")
    else:
        print("Sets A and B contain the same number of nodes.")
    print("-------------------------------------------------------------------")
    # Check for connectivity
    disconnected_nodes_a = [node for node in set_a if all((node, b) not in distances for b in set_b)]
    disconnected_nodes_b = [node for node in set_b if all((a, node) not in distances for a in set_a)]

    if disconnected_nodes_a or disconnected_nodes_b:
        print("Disconnected nodes found!")
        if disconnected_nodes_a:
            print("Nodes in Set A with no connections:", disconnected_nodes_a)
        if disconnected_nodes_b:
            print("Nodes in Set B with no connections:", disconnected_nodes_b)
        print("-------------------------------------------------------------------")
    else:
        print("All nodes in Set A and Set B have at least one connection.")
        print("-------------------------------------------------------------------")

def eliminate_subtour(subtour, prob, x):
    """Add constraints to eliminate the specific subtour."""
    constraint_name = f"subtour_elimination_{len(prob.constraints)}"  # Give each constraint a unique name
    constraint = pulp.lpSum([x[i][j] for i in subtour for j in subtour if i != j]) <= len(subtour) - 1
    prob += constraint, constraint_name
    return prob.constraints[constraint_name]

def check_edges_in_distances(possible_edges, distances):
    """Check if all edges in possible_edges exist in the distances dictionary."""
    missing_edges = []

    for edge in possible_edges:
        if edge in distances:
            print(f"Edge {edge} has distance: {distances[edge]}")
        else:
            print(f"Edge {edge} is missing in distances")
            missing_edges.append(edge)

    return missing_edges

def solve_tsp(distances, possible_edges, set_1, set_2, plot_initial=True):
    """
    Function to solve the TSP.

    Solve the TSP with constraints ensuring alternating connections between sets.

    Parameters:
    - distances: Dictionary of distances between nodes.
    - possible_edges: List of valid edges.
    - set_1: Nodes in set 1 (kit holders).
    - set_2: Nodes in set 2 (gravity racks).
    - plot_initial: Flag to plot the initial solution.

    Returns:
    - optimal_tour: List of edges in the optimal tour.
    """
    nodes = list(set([key[0] for key in distances.keys()] + [key[1] for key in distances.keys()]))

    # Remove node '0.0.0' because it is specifically visited at the end
    nodes.remove('0.0.0')
    # Check for missing edges
    missing_edges = check_edges_in_distances(possible_edges, distances)

    # If there are missing edges, you might want to handle them before solving the TSP
    if missing_edges:
        print("The following edges are missing from the distances dictionary:", missing_edges)

    # Define the problem
    prob = pulp.LpProblem("Bipartite_TSP", pulp.LpMinimize)

    # Decision variables
    x = pulp.LpVariable.dicts("x", (nodes + ['0.0', '0.0.0'], nodes + ['0.0', '0.0.0']), cat='Binary')

    # Objective function: Minimize the total distance using valid edges from possible_edges
    prob += pulp.lpSum([distances[(i, j)] * x[i][j] for i, j in possible_edges])


    print("1----------------------------------------------------")   # Debugging output
    # Constraints for the starting point 0.0 and ending point 0.0.0
    prob += pulp.lpSum([x['0.0'][j] for j in set_2 if ('0.0', j) in possible_edges]) == 1  # Start at 0.0 and go to set_2
    print("Constraints:")
    for name, constraint in prob.constraints.items():
        print(f"{name}: {constraint}")


    print("2----------------------------------------------------")   # Debugging output
    prob += pulp.lpSum([x[i]['0.0.0'] for i in set_1 if (i, '0.0.0') in possible_edges]) == 1  # Go from set_1 to 0.0.0
    print("Constraints:")
    for name, constraint in prob.constraints.items():
        print(f"{name}: {constraint}")


    print("4----------------------------------------------------")  # Debugging output
    for node in set_2:
        prob += pulp.lpSum([x[node][j] for j in set_1 if (node, j) in possible_edges]) <= 1  # Outgoing from set_2 to set_1
        prob += pulp.lpSum([x[i][node] for i in set_1 if (i, node) in possible_edges]) <= 1  # Incoming from set_1 to set_2
        print("Constraints:")
        for name, constraint in prob.constraints.items():
            print(f"{name}: {constraint}")

    print("5----------------------------------------------------")  # Debugging output
    # Flow conservation constraints for Set B:
    for node in set_1:
        prob += pulp.lpSum([x[i][node] for i in set_2 if (i, node) in possible_edges]) == 1  # Incoming to Set 2
        prob += pulp.lpSum([x[node][j] for j in set_2 + ['0.0.0'] if (node, j) in possible_edges]) == 1  # Outgoing from Set 2
        print("Constraints:")
        for name, constraint in prob.constraints.items():
            print(f"{name}: {constraint}")

    print("6----------------------------------------------------")  # Debugging output
    # Incoming = Outgoing
    for node in set_2:
        prob += pulp.lpSum([x[i][node] for i in set_1 + ['0.0'] if i != node and (i, node) in possible_edges]) - pulp.lpSum(
              [x[node][j] for j in set_1 + ['0.0'] if j != node and (node, j) in possible_edges]) == 0
    print("Constraints:")
    for name, constraint in prob.constraints.items():
        print(f"{name}: {constraint}")

    print("7----------------------------------------------------")  # Debugging output
    # Ensure the tour closes by traveling from `0.0.0` back to `0.0`
    prob += pulp.lpSum([x['0.0.0']['0.0']]) == 1 # x_0.0.0_0.0 = 1
    print("Constraints:")
    for name, constraint in prob.constraints.items():
        print(f"{name}: {constraint}")

    # Solve the problem without Subtour Elimination
    prob.solve(pulp.PULP_CBC_CMD(msg=True))

    # Check if optimal solution exists for the problem
    if pulp.LpStatus[prob.status] != 'Optimal':
        print("-------------------------------------------------------------------")
        print("The problem is infeasible or unbounded.")
        print("-------------------------------------------------------------------")
        return None, nodes, x, prob

    # Extract the optimal tour
    optimal_tour = [(i, j) for i, j in possible_edges if pulp.value(x[i][j]) == 1]

    # Print and plot the initial solution
    if plot_initial:
        initial_obj_value = pulp.value(prob.objective)
        print("-------------------------------------------------------------------")
        print("Initial Optimal Solution without Subtour Elimination:")
        for idx, (i, j) in enumerate(optimal_tour):
            print(f"{idx + 1}: {i} -> {j}, Distance: {distances.get((i, j), 'Unknown')}")
        print(f"Initial Optimal objective value without subtour elimination: {initial_obj_value}")
        print("-------------------------------------------------------------------")

    return optimal_tour, nodes, x, prob

def find_subtours(optimal_tour, nodes, set_1, set_2):
    """Find subtours in the current solution."""
    graph = nx.DiGraph()
    graph.add_edges_from(optimal_tour)

    subtours = list(nx.simple_cycles(graph))
    return [subtour for subtour in subtours if len(subtour) < len(nodes) - abs(len(set_1) - len(set_2))]

def iterative_subtour_elimination(distances, possible_edges, set_a, set_b):
    """Solve the TSP with iterative subtour elimination."""
    optimal_tour, nodes, x, prob = solve_tsp(distances, possible_edges, set_a, set_b, plot_initial=True)

    if optimal_tour is None:
        return None

    subtours = find_subtours(optimal_tour, nodes, set_a, set_b)
    iteration_count = 0  # Initialize the iteration counter

    subtour_constraints = []  # List to store constraints for subtour elimination
    while subtours:
        iteration_count += 1
        print(f"Iteration {iteration_count}: Found {len(subtours)} subtour(s)")
        for s_idx, subtour in enumerate(subtours):
            print(f"  Subtour {s_idx + 1}: {subtour}")

        # Remove old subtour constraints
        for constraint in subtour_constraints:
            prob.constraints.pop(constraint, None)  # Safely remove previous constraints

        # Add new subtour constraints
        subtour_constraints = []
        for subtour in subtours:
            subtour_constraint = pulp.lpSum([x[i][j] for i in subtour for j in subtour if i != j]) <= len(subtour) - 1
            prob += subtour_constraint
            subtour_constraints.append(subtour_constraint.name)

        # Re-solve the problem after adding subtour constraints
        prob.solve()

        # Print the objective value after adding subtour constraints
        print(f"Objective value after iteration {iteration_count}: {pulp.value(prob.objective)}")
        print("-------------------------------------------------------------------")

        # Check if the problem is still optimal
        if pulp.LpStatus[prob.status] != 'Optimal':
            # print("-------------------------------------------------------------------")
            print("After subtour elimination, the problem became infeasible.")
            print("-------------------------------------------------------------------")
            return None

        optimal_tour = [(i, j) for i, j in possible_edges if pulp.value(x[i][j]) == 1]
        subtours = find_subtours(optimal_tour, nodes, set_a, set_b)

    # print("-------------------------------------------------------------------")
    print(f"Solution found after {iteration_count} iteration(s)!")
    print(f"Final Objective value after subtour elimination: {pulp.value(prob.objective)}")

    # # Plot the final solution
    # plot_tour(optimal_tour, distances, set_a, set_b, possible_edges,
    #           title=f"Final Solution After Subtour Elimination\nObjective Value: {pulp.value(prob.objective)}")
    return optimal_tour

def plot_tour(optimal_tour, distances, set_a, set_b, possible_edges, title):
    """Plot the optimal tour on the bipartite graph."""
    B = nx.Graph()

    # Add nodes to the graph
    B.add_nodes_from(set_a, bipartite=0)
    B.add_nodes_from(set_b, bipartite=1)
    B.add_node('0.0.0')

    # Add edges to the graph for all possible connections in possible_edges
    for (i, j) in possible_edges:
        B.add_edge(i, j)

    # Define positions for the nodes in the graph
    pos = {node: (1, i) for i, node in enumerate(set_a)}
    pos.update({node: (3, i) for i, node in enumerate(set_b)})
    pos['0.0.0'] = (2, -1)  # Position '0.0.0' below

    # Draw the full bipartite graph with light edges
    plt.figure(figsize=(8, 5))
    nx.draw(B, pos, with_labels=True,
            node_color=['lightblue' if node in set_a else ('lightgreen' if node in set_b else 'lightcoral') for node in
                        B.nodes()], edge_color='gray', alpha=0.5)

    # Highlight the optimal tour with numbered labels
    nx.draw_networkx_edges(B, pos, edgelist=optimal_tour, edge_color='red', width=2, arrows=True, arrowsize=20,
                           arrowstyle='-|>')

    edge_labels = {(i, j): f"{idx + 1}\n{distances.get((i, j), 'Unknown')}" for idx, (i, j) in enumerate(optimal_tour)}
    nx.draw_networkx_edge_labels(B, pos, edge_labels=edge_labels, font_color='blue')

    # Set title dynamically with the total number of connections and objective value
    # plt.title(f"{title}\nTotal Connections: {len(optimal_tour)}")
    plt.suptitle(f"{title}\nTotal Connections: {len(optimal_tour)}", fontsize=10)

    # Display the graph
    plt.show()

def run_exact_tsp(input_data):
    """
    Main function to run the exact TSP solver.
    This function loads data from input_data (dict) and solves the TSP using iterative subtour elimination.
    """
    try:
        # Create the distance matrix from input data (which should now be a dictionary)
        a_to_b_matrix = create_distance_matrices(input_data)  # Adapt this to handle dict input properly

        # Classify nodes into set_1 and set_2
        set_a, set_b = classify_nodes(a_to_b_matrix)

        # Create the distances dictionary using your logic
        distances = create_distances_dict(a_to_b_matrix, set_a, set_b)

        # Extract possible edges
        possible_edges = extract_possible_edges(distances)
        print(possible_edges)

        # Check connectivity and analyze sets for issues
        check_connectivity(set_a, set_b, distances)
        analyze_sets(set_a, set_b, distances)

        # Solve the TSP with iterative subtour elimination
        exact_tour = iterative_subtour_elimination(distances, possible_edges, set_a, set_b)

        if exact_tour:
            # Reconstruct the tour and calculate total cost
            ordered_tour = reconstruct_tour(exact_tour, start_node='0.0')
            exact_tour_cost = sum(distances.get((i, j), 0) for i, j in ordered_tour)
            time_details = [{"from": i, "to": j, "distance": distances.get((i, j), 'Unknown')} for i, j in ordered_tour]

            return ordered_tour, exact_tour_cost, time_details
        else:
            return None, None, None

    except Exception as e:
        print(f"Error in exact method: {e}")
        return None, None, None

def reconstruct_tour(tour_edges, start_node):
    """
    Reconstructs the tour starting from the given start_node.
    """
    # Build a mapping from each node to its neighbor, nodes_sequence
    nodes_seq = {}
    for i, j in tour_edges:
        nodes_seq[i] = j

    # Reconstruct the ordered tour
    ordered_tour = []
    current_node = start_node
    visited = set()
    while True:
        if current_node in visited:
            break
        visited.add(current_node)
        next_node = nodes_seq.get(current_node)
        if next_node is None:
            break
        ordered_tour.append((current_node, next_node))
        current_node = next_node
        if current_node == start_node:
            break

    return ordered_tour
