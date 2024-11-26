import networkx as nx
import matplotlib.pyplot as plt
from parse_json import *

def create_directed_bipartite_graph(a_to_b_matrix):
    B = nx.DiGraph()  # Directed graph

    # kit_holders to set_1 and gravity_racks to set_2
    set_1 = [node for node in a_to_b_matrix.index if len(node.split('.')) == 2 or node == '0.0']  # Includes 0.0 as part of set_1
    set_2 = [node for node in a_to_b_matrix.index if len(node.split('.')) == 3 or node == '0.0.0']  # Includes 0.0.0 as part of set_2

    # Add nodes for set_1 and set_2
    for point_a in set_1:
        B.add_node(point_a, bipartite=0)  # Set 1 on one side
    for point_b in set_2:
        B.add_node(point_b, bipartite=1)  # Set 2 on the other side

    # Print the relevant rows and columns of the distance matrix to check if edges should exist
    print("Distance matrix for 0.0 to set_2 and set_1 to 0.0.0")
    print(a_to_b_matrix.loc[['0.0', '1.1', '1.2'], ['1.1.1', '1.1.2', '0.0.0']])

    # 1. 0.0 can give edges to set_2 (e.g., 1.1.1, 1.1.2)
    for point_b in set_2:
        if point_b != '0.0.0':  # Skip 0.0.0
            weight = a_to_b_matrix.at['0.0', point_b]
            # print(f"Checking edge 0.0 -> {point_b}, weight: {weight}")  # Debugging output
            if weight < 1000000:  # Ensure valid connection
                B.add_edge('0.0', point_b, weight=weight)

    # 2. Set_1 (e.g., 1.1, 1.2) can give edges to 0.0.0
    for point_a in set_1:
        if point_a != '0.0':  # Skip 0.0 itself
            weight = a_to_b_matrix.at[point_a, '0.0.0']
            # print(f"Checking edge {point_a} -> 0.0.0, weight: {weight}")  # Debugging output
            if weight < 1000000:  # Ensure valid connection
                B.add_edge(point_a, '0.0.0', weight=weight)

    # 3. 0.0.0 has one edge to 0.0 with cost 1
    B.add_edge('0.0.0', '0.0', weight=1)

    # 4. Set_2 (e.g., 1.1.1, 1.1.2) can connect bidirectionally with set_1 (e.g., 1.1, 1.2)
    for point_a in set_1:
        for point_b in set_2:
            if point_a != '0.0' and point_b != '0.0.0':  # Skip special nodes
                weight_a_to_b = a_to_b_matrix.at[point_a, point_b]
                weight_b_to_a = a_to_b_matrix.at[point_b, point_a]
                # print(f"Checking edge {point_a} -> {point_b}, weight: {weight_a_to_b}")  # Debugging output
                # print(f"Checking edge {point_b} -> {point_a}, weight: {weight_b_to_a}")  # Debugging output
                if weight_a_to_b < 1000000:  # Valid connection
                    B.add_edge(point_a, point_b, weight=weight_a_to_b)
                if weight_b_to_a < 1000000:  # Valid reverse connection
                    B.add_edge(point_b, point_a, weight=weight_b_to_a)

    # # Print the edges to verify creation
    # print("Directed edges created in the bipartite graph:")
    # for edge in B.edges(data=True):
    #     print(f"{edge[0]} -> {edge[1]} : {edge[2]}")

    return B, set_1, set_2


# Plot the directed bipartite graph
def plot_directed_bipartite_graph(B, set_1, set_2):
    pos = {}
    pos.update((node, (1, index)) for index, node in enumerate(set_1))  # Position for set_1 on the left
    pos.update((node, (0, index)) for index, node in enumerate(set_2))  # Position for set_2 on the right

    plt.figure(figsize=(14, 8))

    # Draw nodes
    nx.draw(B, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold',
            arrows=True, connectionstyle="arc3,rad=0.2")

    # Draw edges with labels indicating direction and weight
    edge_labels = {(u, v): f"{d['weight']}" for u, v, d in B.edges(data=True)}
    nx.draw_networkx_edge_labels(B, pos, edge_labels=edge_labels, font_color='red', font_size=8)

    # Draw arrows separately to make sure they are visible
    nx.draw_networkx_edges(B, pos, arrows=True, arrowstyle='-|>', arrowsize=20, connectionstyle="arc3,rad=0.2")

    plt.title('Directed Bipartite Graph (Set_1 and Set_2)')
    plt.show()


# # Example usage
# json_file_path = 'random_json_TEST.json'
# a_to_b_matrix = create_distance_matrices_from_json(json_file_path)
#
# # Create and plot the bipartite graph
# B, set_1, set_2 = create_directed_bipartite_graph(a_to_b_matrix)
# plot_directed_bipartite_graph(B, set_1, set_2)
