import networkx as nx
import matplotlib.pyplot as plt

def create_bipartite_graph(a_to_b_matrix, b_to_a_matrix):
    B = nx.Graph()

    #Αdd nodes from kit holders (set_1) and start node
    set_1 = list(a_to_b_matrix.index)
    for point_a in set_1:
        B.add_node(point_a, bipartite=0)

    #Add nodes from gravity racks (set_2)
    set_2 = list(a_to_b_matrix.columns)
    for point_b in set_2:
        B.add_node(point_b, bipartite=1)

    if '0.0.0' not in set_2:
        set_2.append('0.0.0')

    #Add edges with weights from a_to_b_matrix and b_to_a_matrix
    for point_a in set_1:
        for point_b in set_2:
            weight_a_to_b = a_to_b_matrix.at[point_a, point_b]  #the weight from kit holder to gravity rack
            weight_b_to_a = b_to_a_matrix.at[point_b, point_a]  #the weight from gravity rack to kit holder
            B.add_edge(point_a, point_b, weight_a_to_b=weight_a_to_b, weight_b_to_a=weight_b_to_a)

    return B, set_1, set_2

#plot the bipartite graph
def plot_bipartite_graph(B):
    pos = nx.bipartite_layout(B, nodes=[n for n, d in B.nodes(data=True) if d['bipartite'] == 0])

    plt.figure(figsize=(14, 8))
    nx.draw(B, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold', arrows=True, arrowsize=20, arrowstyle='-|>')

    edge_labels = {(u, v): f"A→B: {d['weight_a_to_b']}, B→A: {d['weight_b_to_a']}" for u, v, d in B.edges(data=True)}
    nx.draw_networkx_edge_labels(B, pos, edge_labels=edge_labels, font_color='red', font_size=7)

    plt.title('Bipartite Graph')
    plt.show()
