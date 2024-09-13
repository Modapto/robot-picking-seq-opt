import json
import pulp
import networkx as nx
import matplotlib.pyplot as plt


def load_data(json_file):
    """Load the JSON file and extract the distance matrix."""
    with open(json_file, 'r') as file:
        data = json.load(file)
    distance_matrix = data['data']['distanceMatrix']
    return distance_matrix


def classify_nodes(distance_matrix):
    """Classify nodes into set A and set B dynamically based on the distance matrix."""
    set_aa = set()
    set_bb = set()
    set_a = list()
    set_b = list()

    for entry in distance_matrix:
        pointA = entry['pointA']
        pointB = entry['pointB']

        # Skip the entry if either pointA or pointB is '0.0.0'
        if pointA == '0.0.0' or pointB == '0.0.0':
            continue

        # Add pointA to set_a and pointB to set_b
        set_aa.add(pointA)
        set_bb.add(pointB)

    for i in set_aa:
        set_a.append(i)

    for j in set_bb:
        set_b.append(j)

    return set_aa, set_bb, set_a, set_b


def create_distances_dict(distance_matrix, set_a, set_b):
    """Create a dictionary of distances from the distance matrix with specific rules applied."""
    distances = {}

    for entry in distance_matrix:
        pointA = entry['pointA']
        pointB = entry['pointB']
        aToBDist = entry['aToBDist']
        bToADist = entry['bToADist']

        # Rule A: Do not allow connections from Set A to the starting point (0.0.0)
        if pointA in set_a and pointB == '0.0.0':
            continue  # Skip this connection

        # Rule B: Allow connections from 0.0.0 to Set A only if aToBDist is non-zero
        if pointB in set_a and pointA == '0.0.0' and aToBDist != 0:
            distances[(pointA, pointB)] = aToBDist
            continue

        # Rule C: Allow connections from Set B to 0.0.0 based on bToADist
        if pointA in set_b and pointB == '0.0.0' and bToADist != 0:
            distances[(pointA, pointB)] = bToADist  # Capture the Set B to 0.0.0 connections
            continue

        # Allow reverse connections from 0.0.0 to Set B if bToADist is non-zero (to capture 1.1 -> 0.0.0, etc.)
        if pointB in set_b and pointA == '0.0.0' and bToADist != 0:
            distances[(pointB, pointA)] = bToADist  # Capture reverse connections
            continue

        # Rule D: Allow connections between Set A and Set B and vice versa, provided distances are non-zero
        if (pointA in set_a and pointB in set_b) or (pointA in set_b and pointB in set_a):
            if aToBDist != 0:
                distances[(pointA, pointB)] = aToBDist
            if bToADist != 0:
                distances[(pointB, pointA)] = bToADist

    return distances


def extract_possible_edges(distances):
    """Extract possible edges based on the provided distances."""
    return [(i, j) for (i, j) in distances.keys()]


def check_connectivity(SetA, SetB, distances):
    # Check if there are connections between Set A and Set B
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


def solve_tsp(distances, possible_edges, SetA, SetB, plot_initial=True):
    """Solve the TSP without subtour elimination, ensuring feasible connections."""
    nodes = list(set([key[0] for key in distances.keys()] + [key[1] for key in distances.keys()]))
    nodes.remove('0.0.0')

    # Define the problem
    prob = pulp.LpProblem("Bipartite_TSP", pulp.LpMinimize)

    # Decision variables
    x = pulp.LpVariable.dicts("x", (nodes + ['0.0.0'], nodes + ['0.0.0']), cat='Binary')

    # Objective function: Minimize the total distance using valid edges from possible_edges
    prob += pulp.lpSum([distances[(i, j)] * x[i][j] for i, j in possible_edges])
    # DEFAULT_LARGE_VALUE = 1000000
    # prob += pulp.lpSum([distances[(i, j)] * x[i][j] for i, j in possible_edges if
    #                     distances.get((i, j), DEFAULT_LARGE_VALUE) != 0 and i != j])

    # Constraints for the starting point 0.0.0 and sets
    prob += pulp.lpSum([x['0.0.0'][j] for j in SetA if ('0.0.0', j) in possible_edges]) == 1
    prob += pulp.lpSum([x[i]['0.0.0'] for i in SetB if (i, '0.0.0') in possible_edges]) == 1

    # Flow conservation constraints for Set A:
    for node in SetA:
        prob += pulp.lpSum([x[node][j] for j in SetB if (node, j) in possible_edges]) <= 1
        prob += pulp.lpSum([x[i][node] for i in SetB if (i, node) in possible_edges]) <= 1

    # Flow conservation constraints for Set B:
    for node in SetB:
        prob += pulp.lpSum([x[i][node] for i in SetA if (i, node) in possible_edges]) == 1  # Incoming to Set B
        prob += pulp.lpSum([x[node][j] for j in SetA + ['0.0.0'] if (node, j) in possible_edges]) == 1  # Outgoing from Set B

    # Incoming = Outgoing
    for node in SetA:
        prob += pulp.lpSum([x[i][node] for i in SetB + ['0.0.0'] if i != node and (i, node) in possible_edges]) - pulp.lpSum(
              [x[node][j] for j in SetB + ['0.0.0'] if j != node and (node, j) in possible_edges]) == 0

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
        # plot_tour(optimal_tour, distances, SetA, SetB, possible_edges,
        #           title=f"Initial Solution Without Subtour Elimination\nObjective Value: {pulp.value(prob.objective)}")

    return optimal_tour, nodes, x, prob


def find_subtours(optimal_tour, nodes, setA, setB):
    """Find subtours in the current solution."""
    graph = nx.DiGraph()
    graph.add_edges_from(optimal_tour)

    subtours = list(nx.simple_cycles(graph))
    return [subtour for subtour in subtours if len(subtour) < len(nodes)-(len(setA) - len(setB)) ] # length of Grav. Racks - length of Kit Holders for (unequal case)

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


# def main(json_file):
#     """Main function to load data, solve TSP, and plot the result."""
#     distance_matrix = load_data(json_file)
#
#     set_aa, set_bb, set_a, set_b = classify_nodes(distance_matrix)
#
#     distances = create_distances_dict(distance_matrix, set_a, set_b)
#     possible_edges = extract_possible_edges(distances)
#
#     check_connectivity(set_a, set_b, distances)
#     analyze_sets(set_a, set_b, distances)
#
#     optimal_tour = iterative_subtour_elimination(distances, possible_edges, set_a, set_b)
#
#     if optimal_tour is None:
#         return
#
#     print("Optimal Tour:")
#     for idx, (i, j) in enumerate(optimal_tour):
#         print(f"{idx + 1}: {i} -> {j}, Distance: {distances.get((i, j), 'Unknown')}")


def run_exact_tsp_remote(json_data):
    """
    Main function to run the exact TSP solver.
    This function loads data, classifies nodes, checks connectivity,
    and solves the TSP using iterative subtour elimination.
    """
    try:
        # Load the distance matrix and classify nodes
        distance_matrix = json_data['data']['distanceMatrix']
        set_aa, set_bb, set_a, set_b = classify_nodes(distance_matrix)
        distances = create_distances_dict(distance_matrix, set_a, set_b)
        possible_edges = extract_possible_edges(distances)

        # Check connectivity and analyze sets
        check_connectivity(set_a, set_b, distances)
        analyze_sets(set_a, set_b, distances)

        # Solve the TSP with iterative subtour elimination
        exact_tour = iterative_subtour_elimination(distances, possible_edges, set_a, set_b)
        # Build a mapping from each node to its successor
        successors = {}
        for i, j in exact_tour:
            successors[i] = j

        # Reconstruct the tour starting from '0.0.0' and build time_details
        time_details = []
        exact_tour_cost = 0
        current_node = '0.0.0'
        visited = set()
        while True:
            if current_node in visited:
                break
            visited.add(current_node)
            next_node = successors.get(current_node)
            if next_node is None:
                break
            distance = distances.get((current_node, next_node), 'Unknown')
            time_details.append({"from": current_node, "to": next_node, "distance": distance})
            if isinstance(distance, (int, float)):
                exact_tour_cost += distance
            current_node = next_node
            if current_node == '0.0.0':
                break
        # # Calculate the total cost of the exact tour
        # exact_tour_cost = sum(distances.get((i, j), 0) for i, j in exact_tour)
        # time_details = [{"from": i, "to": j, "distance": distances.get((i, j), 'Unknown')} for i, j in exact_tour]

        return exact_tour, exact_tour_cost, time_details

    except ValueError as e:
        print(f"Error in exact method: {e}")
        return None, None, None


def run_exact_tsp_local(json_file_path):
    """
    Main function to run the exact TSP solver.
    This function loads data, classifies nodes, checks connectivity,
    and solves the TSP using iterative subtour elimination.
    """
    try:
        # Load the distance matrix and classify nodes
        distance_matrix = load_data(json_file_path)
        set_aa, set_bb, set_a, set_b = classify_nodes(distance_matrix)
        distances = create_distances_dict(distance_matrix, set_a, set_b)
        possible_edges = extract_possible_edges(distances)

        # Check connectivity and analyze sets
        check_connectivity(set_a, set_b, distances)
        analyze_sets(set_a, set_b, distances)

        # Solve the TSP with iterative subtour elimination
        exact_tour = iterative_subtour_elimination(distances, possible_edges, set_a, set_b)
        # Build a mapping from each node to its successor
        successors = {}
        for i, j in exact_tour:
            successors[i] = j

        # Reconstruct the tour starting from '0.0.0' and build time_details
        time_details = []
        exact_tour_cost = 0
        current_node = '0.0.0'
        visited = set()
        while True:
            if current_node in visited:
                break
            visited.add(current_node)
            next_node = successors.get(current_node)
            if next_node is None:
                break
            distance = distances.get((current_node, next_node), 'Unknown')
            time_details.append({"from": current_node, "to": next_node, "distance": distance})
            if isinstance(distance, (int, float)):
                exact_tour_cost += distance
            current_node = next_node
            if current_node == '0.0.0':
                break

        return exact_tour, exact_tour_cost, time_details

    except ValueError as e:
        print(f"Error in exact method: {e}")
        return None, None, None


# # Run the main function with the provided JSON file
# json_file = 'random_json_input.json'



### Run the main function with the provided JSON file
# json_file = 'baby_example.json' # Equal Sets A and B
# json_file = 'small2x4.json' # Not Equal Sets A and B
# json_file = 'small.json' # Equal Sets A and B # 8x8
# json_file = 'big.json'
# json_file = 'gr40xkh20.json'  # 40x20
# json_file = 'gr40xkh40.json' # 40x40
# json_file = 'input_GR_20x2x10_KH_4x5_Run_2.json' # 400 x 20
# json_file = 'input_GR_50x2x10_KH_4x5_Run_2.json' # 1000 x 20
# json_file = 'input_GR_100x2x10_KH_4x5_Run_3.json' # 2000 x 20
# main(json_file)
