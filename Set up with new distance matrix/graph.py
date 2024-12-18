import networkx as nx
import matplotlib.pyplot as plt
from distance_matrix_creation import *

def create_directed_bipartite_graph_new(a_to_b_matrix):
    B = nx.DiGraph()

    set_1 = [node for node in a_to_b_matrix.index if len(node.split('.')) == 2]  # Kit holders
    set_2 = [node for node in a_to_b_matrix.index if len(node.split('.')) == 3]  # Gravity racks

    B.add_nodes_from(set_1, bipartite=0)
    B.add_nodes_from(set_2, bipartite=1)

    for point_a in set_1:
        for point_b in set_2:
            weight_a_to_b = a_to_b_matrix.at[point_a, point_b]
            weight_b_to_a = a_to_b_matrix.at[point_b, point_a]

            if weight_a_to_b < 1000000:
                B.add_edge(point_a, point_b, weight=weight_a_to_b)
            if weight_b_to_a < 1000000:
                B.add_edge(point_b, point_a, weight=weight_b_to_a)

    return B, set_1, set_2


def plot_directed_bipartite_graph(B, set_1, set_2):

    pos = {}
    pos.update((node, (1, index)) for index, node in enumerate(set_1))
    pos.update((node, (0, index)) for index, node in enumerate(set_2))

    plt.figure(figsize=(14, 8))

    nx.draw(B, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold',
            arrows=True, connectionstyle="arc3,rad=0.2")

    edge_labels = {(u, v): f"{d['weight']}" for u, v, d in B.edges(data=True)}
    nx.draw_networkx_edge_labels(B, pos, edge_labels=edge_labels, font_color='red', font_size=8)

    nx.draw_networkx_edges(B, pos, arrows=True, arrowstyle='-|>', arrowsize=20, connectionstyle="arc3,rad=0.2")

    plt.title('Directed Bipartite Graph (Set_1 and Set_2)')
    plt.show()

B, set_1, set_2 = create_directed_bipartite_graph_new(distance_matrix)
plot_directed_bipartite_graph(B, set_1, set_2)
