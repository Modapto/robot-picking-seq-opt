import copy
from co_pilot_sim_GR import filter_distance_matrix
from co_exact_method import run_exact_tsp
from co_method_linear import linear_picking, total_cost
from co_GraphCreation import create_directed_bipartite_graph
from co_parse_json import create_distance_matrices

def normalise_kh_sequences(raw_seqs):
    """
    Accepts either
      [["KH002", "KH001"], …]                         # v2-old
      [[{"1": "KH001"}, {"2": "KH003"}], …]           # new
    and always returns List[List[str]].
    """
    if raw_seqs and raw_seqs[0] and isinstance(raw_seqs[0][0], dict):
        return [
            [next(iter(slot.values())) for slot in seq]
            for seq in raw_seqs
        ]
    return raw_seqs

def generate_kh_configuration(kh_setup, kit_holders_template):
    configured_kh = {}
    for idx, kh_id in enumerate(kh_setup, start=1):
        if kh_id == "EMPTY":
            continue
        if kh_id in kit_holders_template:
            kh_data = copy.deepcopy(kit_holders_template[kh_id])
            for i, content in enumerate(kh_data["contents"], start=1):
                content["position"] = f"{idx}.{i}"
            configured_kh[f"KH{idx}"] = {
                "kh_position": str(idx),
                "contents": kh_data["contents"]
            }
        else:
            configured_kh[f"KH{idx}"] = {"kh_position": kh_id, "contents": []}
    return configured_kh

def annotate_component_in_time_details(time_details, gr_nodes, kh_nodes):
    enriched = []
    current_component = None

    for step in time_details:
        src = step["from"]
        dst = step["to"]
        enriched_step = step.copy()

        # GR → KH → robot places component
        if src in gr_nodes and dst in kh_nodes:
            current_component = gr_nodes[src]
            enriched_step["component_placed"] = current_component

        # 0.0 → GR → robot picks component
        elif src == "0.0" and dst in gr_nodes:
            current_component = gr_nodes[dst]
            enriched_step["component_picked"] = current_component

        # KH → GR (robot picks next component) — OPTIONAL, if needed
        elif src in kh_nodes and dst in gr_nodes:
            current_component = gr_nodes[dst]
            enriched_step["component_picked"] = current_component

        enriched.append(enriched_step)

    return enriched

def calculate_full_sequence_cost(distance_matrix, configuration, method="exact"):
    working_matrix = distance_matrix.copy()
    last_node_visited = "0.0"
    total_method_cost = 0
    full_tour = []
    segmented_details = []
    kh_sequences = configuration["kh_sequences"]

    for i, kh_setup in enumerate(kh_sequences):
        print(f"\n>>> Processing KH Setup {i + 1}: {kh_setup}")
        if i > 0:
            print(f"Duplicating last visited node ({last_node_visited}) as '0.0'...")
            new_matrix = [edge for edge in working_matrix if not edge["edge"].startswith("(0.0,")]
            for edge in distance_matrix:
                if edge["edge"].startswith(f"({last_node_visited},"):
                    new_edge = {"edge": edge["edge"].replace(f"({last_node_visited},", "(0.0,"),
                                "distance": edge["distance"]}
                    new_matrix.append(new_edge)
            working_matrix = new_matrix

        kh_config = generate_kh_configuration(kh_setup, configuration["kit_holders_template"])
        filtered_matrix = filter_distance_matrix(working_matrix,
                                                 {"containers": configuration["containers"], "kit_holders": kh_config})
        end_node = None if i < len(kh_sequences) - 1 else "0.0"

        if method == "exact":
            tour, cost, time_details = run_exact_tsp(
                {"data": {"distanceMatrix": filtered_matrix, "start_node": "0.0", "end_node": end_node}})
            if i < len(kh_sequences) - 1:
                for j in range(len(tour) - 1, -1, -1):
                    if tour[j][1] == "0.0.0":
                        last_node_visited = tour[j][0]
                        tour = tour[:j]
                        time_details = [step for step in time_details if step["to"] not in ["0.0.0", "0.0"]]
                        cost = sum(step["distance"] for step in time_details)
                        break
                print(f"Trimmed tour, last node: {last_node_visited}")
        else:  # linear
            a_to_b_matrix = create_distance_matrices({"data": {"distanceMatrix": filtered_matrix}})
            B, set_1, set_2 = create_directed_bipartite_graph(a_to_b_matrix)
            tour_data = linear_picking(B, "0.0", "0.0" if i == len(kh_sequences) - 1 else None, set_1, set_2)
            cost, time_details = total_cost(B, tour_data["tour"])
            # Normalize time_details to use "distance" instead of "totalTime"
            time_details = [{"from": step["from"], "to": step["to"], "distance": step["totalTime"]} for step in
                            time_details]
            tour = [(step["from"], step["to"]) for step in time_details]
            if i < len(kh_sequences) - 1:
                for j in range(len(tour) - 1, -1, -1):
                    if tour[j][1] == "0.0.0":
                        last_node_visited = tour[j][0]
                        if last_node_visited == "0.0" and j > 0:  # Use previous node if "0.0"
                            last_node_visited = tour[j - 1][0]
                        tour = tour[:j]
                        time_details = [step for step in time_details if step["to"] not in ["0.0.0", "0.0"]]
                        cost = sum(step["distance"] for step in time_details)
                        break
                print(f"Trimmed linear tour, last node: {last_node_visited}")

        total_method_cost += cost
        full_tour.extend(
            tour if i == 0 else [(last_node_visited, step[1]) if step[0] == "0.0" else step for step in tour[1:]])
        segment_details = time_details if i == 0 else [
                                                          {"from": last_node_visited, "to": time_details[0]["to"],
                                                           "distance": time_details[0]["distance"]}
                                                      ] + [step for step in time_details[1:]]
        segmented_details.append(segment_details)

    return total_method_cost, full_tour, segmented_details
