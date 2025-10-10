import networkx as nx

def create_directed_bipartite_graph(a_to_b_matrix,active_kh_positions, large_number=1000000):
    """
    Creates a directed bipartite graph based on a distance matrix.
    Special cases:
        - 0.0 → GR (except 0.0.0)
        - KH → 0.0.0 (except 0.0)
        - 0.0.0 → 0.0 (final return)
        - KH ↔ GR (bidirectional)
        - KH → KH (excluding 0.0)

    """
    B = nx.DiGraph()

    # Define node groups
    set_1 = [node for node in a_to_b_matrix.index if len(node.split('.')) == 2 or node == '0.0']
    set_2 = [node for node in a_to_b_matrix.index if len(node.split('.')) == 3 or node == '0.0.0']

    # Add nodes with bipartite attributes
    for node in set_1:
        B.add_node(node, bipartite=0)
    for node in set_2:
        B.add_node(node, bipartite=1)

    # 1. Add edges from 0.0 → GR (excluding 0.0.0)
    for gr in set_2:
        if gr != '0.0.0':
            weight = a_to_b_matrix.at['0.0', gr]
            if weight < 1000000:
                B.add_edge('0.0', gr, weight=weight)
                # print(f"Start node 0.0 connects to: {gr}")

    # 2. Add edges from KH → 0.0.0 (excluding 0.0)
    for kh in set_1:
        if kh != '0.0':
            weight = a_to_b_matrix.at[kh, '0.0.0']
            if weight < 1000000:
                B.add_edge(kh, '0.0.0', weight=weight)
                # print(f"{kh} goes to final node 0.0.0")

    # 3. Add final return edge 0.0.0 → 0.0
    B.add_edge('0.0.0', '0.0', weight=1)
    print("Final return from 0.0.0 → 0.0 confirmed")

    # 4. Add bidirectional edges between KH and GR
    for kh in set_1:
        for gr in set_2:
            if kh != '0.0' and gr != '0.0.0':
                weight_kh_to_gr = a_to_b_matrix.at[kh, gr]
                weight_gr_to_kh = a_to_b_matrix.at[gr, kh]
                if weight_kh_to_gr < 1000000:
                    B.add_edge(kh, gr, weight=weight_kh_to_gr)
                if weight_gr_to_kh < 1000000:
                    B.add_edge(gr, kh, weight=weight_gr_to_kh)
    print("KH nodes:", [n for n in set_1 if n != "0.0"])

    # Step 5: KH → KH
    for u in active_kh_positions:
        for v in active_kh_positions:
            if u != v and u != '0.0' and v != '0.0':
                weight = a_to_b_matrix.at[u, v]
                # print(f"Checking KH→KH candidate {u}->{v}: weight={weight}")
                if weight < large_number:
                    # print(f"  ✔ adding {u}->{v}")
                    B.add_edge(u, v, weight=weight)
    # 6. Add GR → GR (excluding 0.0.0)
    for u in set_2:
        for v in set_2:
            if u != v and u != "0.0.0" and v != "0.0.0":
                try:
                    weight = a_to_b_matrix.at[u, v]
                    if weight < 1000000:
                        B.add_edge(u, v, weight=weight)
                        # print(f"GR → GR edge added: {u} → {v} | weight = {weight}")
                except KeyError:
                    continue

    return B, set_1, set_2


# def main():
#     for i, kh_setup in enumerate(kh_sequences):
#         print(f"\n>>> Running Phase {i + 1} with KH Setup: {kh_setup}")
#
#         # Generate KH configuration for the current phase
#         kh_config = generate_kh_configuration(kh_setup, kit_holders_template)
#
#         # Generate filtered distance matrix
#         filtered_matrix = filter_distance_matrix(distance_matrix, {
#             "containers": current_config["containers"],
#             "kit_holders": kh_config
#         })
#         # Duplicate Last Visited Node for Next Phase
#         if i > 0:
#             duplicated_node = last_node_visited
#             renamed_node = "0.0"
#             # print(f"Duplicating last visited node ({duplicated_node}) and renaming duplicate as `{renamed_node}`.")
#             if duplicated_node not in kh_setup:
#                 kh_setup.insert(0, duplicated_node)
#                 # print(f"Updated kh_setup: {kh_setup}")
#
#             # Use distance_matrix for duplication
#             new_filtered_matrix = filtered_matrix.copy()
#             duplicated_edges_added = 0
#             for edge in distance_matrix:  # Source from full distance_matrix
#                 if edge["edge"].startswith(f"({duplicated_node},"):
#                     new_edge = {
#                         "edge": edge["edge"].replace(f"({duplicated_node},", f"({renamed_node},"),
#                         "distance": edge["distance"] + 2000  # Match filter_distance_matrix adjustment
#                     }
#                     # Replace existing "0.0" edge
#                     new_filtered_matrix = [e for e in new_filtered_matrix if e["edge"] != new_edge["edge"]]
#                     new_filtered_matrix.append(new_edge)
#                     duplicated_edges_added += 1
#                     # print(f"Added duplicated edge: {new_edge}")
#                 if edge["edge"].endswith(f", {duplicated_node})"):
#                     new_edge = {
#                         "edge": edge["edge"].replace(f", {duplicated_node})", f", {renamed_node})"),
#                         "distance": edge["distance"] + 2000
#                     }
#                     new_filtered_matrix.append(new_edge)
#                     duplicated_edges_added += 1
#             filtered_matrix = new_filtered_matrix
#
#         # print(filtered_matrix)
#         matrix = create_distance_matrices({"data": {"distance_matrix": filtered_matrix}})
#         # Remove potential whitespaces from row/column labels
#         matrix.index = matrix.index.str.strip()
#         matrix.columns = matrix.columns.str.strip()
#
#         # print(
#             # f"a_to_b_matrix created with shape: {a_to_b_matrix.shape if hasattr(a_to_b_matrix, 'shape') else 'unknown'}")
#         print("Matrix Index (rows):", matrix.index.tolist()[:50])
#         print("Matrix Columns:", matrix.columns.tolist()[:50])
#         print(matrix.iloc[:25, :25])
#         active_kh_positions = []
#         for kh_data in kh_config.values():
#             for content in kh_data["contents"]:
#                 active_kh_positions.append(content["position"])
#         # print("✅ Active KH Positions:", active_kh_positions)
#
#         # Create bipartite graph
#         print("Creating directed bipartite graph...")
#         B, set_1, set_2 = create_directed_bipartite_graph(matrix,active_kh_positions)
#         # print(f"Graph B nodes: {len(B.nodes())}, edges: {len(B.edges())}")
#         print(f"Set 1 (kit holders): {set_1}")
#         print(f"Set 2 (gravity racks): {set_2}")
#     # Example usage
#     print_sample_edges_with_weights(B)
#
#
# def print_sample_edges_with_weights(B, sample_size=5):
#     categories = {
#         "KH → KH": [],
#         "GR → GR": []
#     }
#
#     for u, v, data in B.edges(data=True):
#         u_parts = u.split('.')
#         v_parts = v.split('.')
#         is_u_gr = len(u_parts) == 3 or u == "0.0.0"
#         is_v_gr = len(v_parts) == 3 or v == "0.0.0"
#         is_u_kh = len(u_parts) == 2 or u == "0.0"
#         is_v_kh = len(v_parts) == 2 or v == "0.0"
#
#         if is_u_kh and is_v_kh and "0.0" not in (u, v):
#             categories["KH → KH"].append((u, v, data["weight"]))
#         elif is_u_gr and is_v_gr and "0.0.0" not in (u, v):
#             categories["GR → GR"].append((u, v, data["weight"]))
#
#     print("Sample Edges by Type with Weights:\n")
#     for label, edges in categories.items():
#         print(f"▶ {label} ({len(edges)} total):")
#         for u, v, w in random.sample(edges, min(len(edges), sample_size)):
#             print(f"   {u} → {v} | weight = {w}")
#         print()
#
# if __name__ == "__main__":
#     # load JSON, templates, and kh_sequences here, then call main()
#     with open("random_json_input_dual.json", "r") as f:
#         input_data = json.load(f)
#         data = input_data["data"]
#
#     distance_matrix       = data["distance_matrix"]
#     containers_template   = data["containers_template"]
#     kit_holders_template  = data["kit_holders_template"]
#     current_config        = data["current_config"]
#     kh_sequences          = data.get("kh_sequences") or [data.get("kh_setup", [])]
#     last_node_visited     = data.get('start_node', '0.0')
#
#     main()

