import networkx as nx
import matplotlib.pyplot as plt
from distance_matrix_creation import *

def create_directed_bipartite_graph(a_to_b_matrix):
    """
    Creates a directed bipartite graph based on a distance matrix.

    Parameters:
    - a_to_b_matrix: DataFrame representing distances between nodes.

    Returns:
    - B: A directed bipartite graph.
    - set_1: Nodes in set_1 (kit holders, including 0.0).
    - set_2: Nodes in set_2 (gravity racks, including 0.0.0).
    """
    B = nx.DiGraph()

    set_1 = [node for node in a_to_b_matrix.index if len(node.split('.')) == 2 or node == '0.0']
    set_2 = [node for node in a_to_b_matrix.index if len(node.split('.')) == 3 or node == '0.0.0']

    B.add_nodes_from(set_1, bipartite=0)
    B.add_nodes_from(set_2, bipartite=1)

    # Add edges based on distance matrix
    for source in a_to_b_matrix.index:
        for target in a_to_b_matrix.columns:
            weight = a_to_b_matrix.at[source, target]
            if weight < 1000000:
                B.add_edge(source, target, weight=weight)

    return B, set_1, set_2


def plot_directed_bipartite_graph(B, set_1, set_2):
    """
    Plots a directed bipartite graph with weights on edges.

    Parameters:
    - B: Directed bipartite graph to plot.
    - set_1: Nodes in set_1 (kit holders).
    - set_2: Nodes in set_2 (gravity racks).
    """
    pos = {}
    pos.update((node, (1, i)) for i, node in enumerate(set_1))
    pos.update((node, (2, i)) for i, node in enumerate(set_2))

    plt.figure(figsize=(14, 8))
    nx.draw(B, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold')
    edge_labels = {(u, v): f"{d['weight']}" for u, v, d in B.edges(data=True)}
    nx.draw_networkx_edge_labels(B, pos, edge_labels=edge_labels, font_color='red', font_size=8)
    plt.title("Directed Bipartite Graph")
    plt.show()


B, set_1, set_2 = create_directed_bipartite_graph(distance_matrix)

# Plot the graph
plot_directed_bipartite_graph(B, set_1, set_2)

# Output graph information
print(f"Graph has {B.number_of_nodes()} nodes and {B.number_of_edges()} edges.")