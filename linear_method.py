# REPOSITORY NAME (c) by the University of Piraues, Greece.
#
# REPOSITORY NAME is licensed under a
# Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <http://creativecommons.org/licenses/by-nc-nd/3.0/>.

# Construct a linear (greedy) picking tour over a bipartite graph.
#
# The heuristic:
#     - Iterates over positions in set_1 in sorted order.
#     - For each position (kit holder), finds the closest matching rack in set_2
#       that has an edge to this position.
#     - From the current tour node, moves to the chosen rack, then from that rack
#       to the corresponding position in set_1.
#     - At the end, if possible, moves from the last node in the tour to end_node.
#
# Distances can optionally be overridden using a precomputed `filtered_matrix`.
#
# Parameters:
#     B (networkx.Graph or networkx.DiGraph): Graph containing nodes and edges with 'weight'.
#     start_node (str): Starting node of the tour (e.g. '0.0').
#     end_node (str): Ending node of the tour (e.g. '0.0.0').
#     set_1 (iterable[str]): Iterable of kit holder nodes (including the start node).
#     set_2 (iterable[str]): Iterable of rack nodes.
#     filtered_matrix (list[dict] or None): Optional list of dictionaries with keys
#         - "edge" (str): String representation of an edge, e.g. "(u, v)".
#         - "distance" (float): Distance value overriding the graph weight.
#
# Returns:
#     dict: A dictionary with keys:
#         - "tour" (list[str]): Sequence of visited nodes.
#         - "total_cost" (float): Total cost of the constructed tour.
def linear_picking(B, start_node, end_node, set_1, set_2, filtered_matrix=None):
    tour = [start_node]
    total_cost = 0
    distance_dict = {edge["edge"]: edge["distance"] for edge in filtered_matrix} if filtered_matrix else {}

    for position in sorted(set_1):
        if position == start_node and len(tour) == 1:  # Skip initial start_node
            continue
        matching_rack = None
        min_distance = float('inf')

        for rack in set_2:
            if B.has_edge(rack, position):
                edge_key = f"({rack}, {position})"
                distance = distance_dict.get(edge_key, B[rack][position]['weight'])
                if distance < min_distance:
                    min_distance = distance
                    matching_rack = rack

        if matching_rack:
            edge_key = f"({tour[-1]}, {matching_rack})"
            distance = distance_dict.get(edge_key, B[tour[-1]][matching_rack]['weight'])
            tour.append(matching_rack)
            total_cost += distance

            edge_key = f"({matching_rack}, {position})"
            distance = distance_dict.get(edge_key, B[matching_rack][position]['weight'])
            tour.append(position)
            total_cost += distance

    if tour[-1] != end_node:
        edge_key = f"({tour[-1]}, {end_node})"
        distance = distance_dict.get(edge_key, B[tour[-1]][end_node]['weight'] if B.has_edge(tour[-1], end_node) else float('inf'))
        if distance != float('inf'):
            tour.append(end_node)
            total_cost += distance

    return {"tour": tour, "total_cost": total_cost}

def total_cost(G, tour, filtered_matrix=None):
    """
    Compute the total cost and time details for a given tour.

    For each consecutive pair of nodes in the tour, the function:
        - Looks up the edge weight either from `filtered_matrix` (if provided) or
          from the graph `G`.
        - If the weight is finite, it is added to the total cost and recorded in
          the time details list.

    Parameters:
        G (networkx.Graph or networkx.DiGraph): Graph containing nodes and edges with 'weight'.
        tour (list[str]): Sequence of nodes representing the tour.
        filtered_matrix (list[dict] or None): Optional list of dictionaries with keys

    Returns:
         - cost (float): Sum of all edge weights along the tour.
         - time_details (list[dict]): Per-edge details with keys:
    """
    cost = 0
    time_details = []
    distance_dict = {edge["edge"]: edge["distance"] for edge in filtered_matrix} if filtered_matrix else {}
    for i in range(len(tour) - 1):
        u, v = tour[i], tour[i + 1]
        edge_key = f"({u}, {v})"
        weight = distance_dict.get(edge_key, G[u][v]['weight'] if u in G and v in G[u] else float('inf'))
        if weight != float('inf'):
            cost += weight
            time_details.append({
                "from": u,
                "to": v,
                "totalTime": weight
            })
    return cost, time_details

