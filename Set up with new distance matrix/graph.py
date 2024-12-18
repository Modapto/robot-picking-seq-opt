import networkx as nx
import matplotlib.pyplot as plt
from distance_matrix_creation import *

def create_directed_bipartite_graph_new(a_to_b_matrix):
    """
    Creates a directed bipartite graph based on the new distance matrix format,
    excluding `0.0` and `0.0.0`.

    Parameters:
    - a_to_b_matrix: DataFrame representing distances between nodes.

    Returns:
    - B: A directed bipartite graph.
    - set_1: Nodes in set_1 (kit holders).
    - set_2: Nodes in set_2 (gravity racks).
    """
    B = nx.DiGraph()

    # Define node sets
    set_1 = [node for node in a_to_b_matrix.index if len(node.split('.')) == 2]  # Kit holders
    set_2 = [node for node in a_to_b_matrix.index if len(node.split('.')) == 3]  # Gravity racks

    # Add nodes
    B.add_nodes_from(set_1, bipartite=0)
    B.add_nodes_from(set_2, bipartite=1)

    # Add edges from set_1 to set_2 and vice versa
    for point_a in set_1:
        for point_b in set_2:
            weight_a_to_b = a_to_b_matrix.at[point_a, point_b]
            weight_b_to_a = a_to_b_matrix.at[point_b, point_a]

            if weight_a_to_b < 1000000:  # Valid connection
                B.add_edge(point_a, point_b, weight=weight_a_to_b)
            if weight_b_to_a < 1000000:  # Valid reverse connection
                B.add_edge(point_b, point_a, weight=weight_b_to_a)

    return B, set_1, set_2


# Function to plot the directed bipartite graph
def plot_directed_bipartite_graph(B, set_1, set_2):
    """
    Plots a directed bipartite graph with weights on edges.

    Parameters:
    - B: Directed bipartite graph to plot.
    - set_1: Nodes in set_1 (kit holders).
    - set_2: Nodes in set_2 (gravity racks).
    """
    pos = {}  # Dictionary to store node positions for plotting
    pos.update((node, (1, index)) for index, node in enumerate(set_1))  # Left positions for set_1
    pos.update((node, (0, index)) for index, node in enumerate(set_2))  # Right positions for set_2

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


# Example Usage
# Assume `a_to_b_matrix` is already created as a DataFrame
B, set_1, set_2 = create_directed_bipartite_graph_new(distance_matrix)
plot_directed_bipartite_graph(B, set_1, set_2)
