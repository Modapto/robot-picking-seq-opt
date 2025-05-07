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

