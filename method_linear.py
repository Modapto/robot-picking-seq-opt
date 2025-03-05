# def linear_picking(B, start_node, end_node, set_1, set_2):
#     """
#     Simulates the industrial workflow with a linear picking sequence.
#
#     Parameters:
#         B (networkx.DiGraph): The directed bipartite graph with distances between nodes.
#         start_node (str): Starting node of the tour (e.g., "0.0").
#         end_node (str): Ending node of the tour (e.g., "0.0.0").
#         set_1 (list): List of kit holder positions.
#         set_2 (list): List of gravity rack positions.
#
#     Returns:
#         dict: A linear picking sequence (tour) and total cost.
#     """
#     tour = [start_node]  # Start from the initial node
#     total_cost = 0
#
#     # Iterate over each position in set_1 sequentially
#     for position in sorted(set_1):  # Ensure positions are processed in order
#         matching_rack = None
#         min_distance = float('inf')
#
#         for rack in set_2:
#             if B.has_edge(rack, position):  # Check if connection exists
#                 distance = B[rack][position]['weight']  # Access the edge weight
#                 if distance < min_distance:
#                     min_distance = distance
#                     matching_rack = rack
#
#         if matching_rack:
#             # Move from current node to the matching rack
#             if B.has_edge(tour[-1], matching_rack):
#                 tour.append(matching_rack)
#                 total_cost += B[tour[-2]][matching_rack]['weight']
#
#             # Move from rack to kit holder position
#             tour.append(position)
#             total_cost += min_distance
#
#     # Return to the end node
#     if tour[-1] != end_node:
#         tour.append(end_node)
#         if B.has_edge(tour[-2], end_node):
#             total_cost += B[tour[-2]][end_node]['weight']
#
#     return {"tour": tour, "total_cost": total_cost}
#
#
# def total_cost(G, tour):
#     """
#     Function to calculate the total cost of a given tour.
#
#     Calculate the total cost of a tour.
#
#     Parameters:
#     - G: A graph representing the problem.
#     - tour: List of nodes representing the tour.
#
#     Returns:
#     - cost: Total cost of the tour.
#     - time_details: List of details for each segment of the tour.
#     """
#     cost = 0
#     time_details = []
#     for i in range(len(tour) - 1):
#         u, v = tour[i], tour[i + 1]
#         if u in G and v in G[u]:
#             weight = G[u][v]['weight']
#             cost += weight
#             time_details.append({
#                 "from": u,
#                 "to": v,
#                 "totalTime": weight
#             })
#     return cost, time_details
#

import networkx as nx

def linear_picking(B, start_node, end_node, set_1, set_2):
    """
    Simulates the industrial workflow with a linear picking sequence.

    Parameters:
        B (networkx.DiGraph): The directed bipartite graph with distances between nodes.
        start_node (str): Starting node of the tour (e.g., "0.0").
        end_node (str): Ending node of the tour (e.g., "0.0.0").
        set_1 (list): List of kit holder positions.
        set_2 (list): List of gravity rack positions.

    Returns:
        dict: A linear picking sequence (tour) and total cost.
    """
    tour = [start_node]  # Start from the initial node
    total_cost = 0

    ### 🚀 **Fix: Ensure we start from the correct last visited node**
    if start_node in B:
        for node in set_2:  # Check all gravity racks
            if B.has_edge(node, start_node):  # If previous last node exists in the matrix
                print(f"🔄 Adjusting start: {start_node} should follow {node}")
                tour.insert(0, node)  # Insert the correct last visited node at the beginning
                total_cost += B[node][start_node]['weight']

    # Iterate over each position in set_1 sequentially
    for position in sorted(set_1):  # Ensure positions are processed in order
        matching_rack = None
        min_distance = float('inf')

        for rack in set_2:
            if B.has_edge(rack, position):  # Check if connection exists
                distance = B[rack][position]['weight']  # Access the edge weight
                if distance < min_distance:
                    min_distance = distance
                    matching_rack = rack

        if matching_rack:
            # Move from current node to the matching rack
            if B.has_edge(tour[-1], matching_rack):
                tour.append(matching_rack)
                total_cost += B[tour[-2]][matching_rack]['weight']

            # Move from rack to kit holder position
            tour.append(position)
            total_cost += min_distance

    # Return to the end node
    if tour[-1] != end_node:
        tour.append(end_node)
        if B.has_edge(tour[-2], end_node):
            total_cost += B[tour[-2]][end_node]['weight']

    return {"tour": tour, "total_cost": total_cost}




def total_cost(G, tour):
    """
    Function to calculate the total cost of a given tour.

    Parameters:
    - G: A graph representing the problem.
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
