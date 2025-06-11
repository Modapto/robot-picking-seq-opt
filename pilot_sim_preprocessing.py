import random
import copy
from itertools import product
from exact_method import run_exact_tsp
from method_linear import linear_picking, total_cost
from GraphCreation import create_directed_bipartite_graph
from parse_json import create_distance_matrices

def generate_all_kh_configurations(kit_holders, num_positions=4):
    kh_keys = list(kit_holders.keys())
    all_combinations = list(product(kh_keys, repeat=num_positions))  # Cartesian product
    random.shuffle(all_combinations)  # Randomize configurations
    return all_combinations

def randomize_kit_holders(kit_holders, configuration):
    new_kit_holders = {}
    for pos_idx, kh_key in enumerate(configuration, start=1):
        kh_data = copy.deepcopy(kit_holders[kh_key])
        new_contents = []

        for i, content in enumerate(kh_data["contents"], start=1):
            content["position"] = f"{pos_idx}.{i}"
            new_contents.append(content)

        new_kit_holders[f"KH{pos_idx}"] = {
            "kh_position": str(pos_idx),
            "contents": new_contents,
        }

    return new_kit_holders

def randomize_containers(containers_template):
    all_components = []
    for container in containers_template.values():
        for content in container["contents"]:
            if content["type"] not in all_components:
                all_components.append(content["type"])

    random.shuffle(all_components)

    new_containers = {}
    for idx, container_key in enumerate(containers_template.keys(), start=1):
        group = 1 if idx <= 7 else 2
        subgroup = idx if group == 1 else idx - 7
        gr_position = f"{group}.{subgroup}"

        component_type = all_components[(idx - 1) % len(all_components)]
        new_contents = [
            {"position": f"{gr_position}.{i}", "type": component_type}
            for i in range(1, 5)
        ]

        new_containers[container_key] = {"gr_position": gr_position, "contents": new_contents}

    return new_containers

def generate_random_configuration(containers, kit_holders):
    all_kh_configs = generate_all_kh_configurations(kit_holders, num_positions=4)
    selected_config = random.choice(all_kh_configs)
    randomized_kit_holders = randomize_kit_holders(kit_holders, selected_config)
    randomized_containers = randomize_containers(containers)
    return {"containers": randomized_containers, "kit_holders": randomized_kit_holders}

def filter_distance_matrix(matrix, random_config):
    filtered_matrix = []
    containers = random_config["containers"]
    kit_holders = random_config["kit_holders"]

    # Transform distance matrix to a lookup dictionary
    matrix_dict = {}
    for entry in matrix:
        edge = entry["edge"].strip("()").split(", ")
        source, target = edge[0], edge[1]
        if source not in matrix_dict:
            matrix_dict[source] = {}
        matrix_dict[source][target] = entry["distance"]

    # Add edges: 0.0 to all gravity racks
    if "0.0" in matrix_dict:
        for target, distance in matrix_dict["0.0"].items():
            filtered_matrix.append({"edge": f"(0.0, {target})", "distance": distance + 2000})

    # Add edges: 0.0.0 to 0.0
    if "0.0.0" in matrix_dict and "0.0" in matrix_dict["0.0.0"]:
        filtered_matrix.append({"edge": "(0.0.0, 0.0)", "distance": matrix_dict["0.0.0"]["0.0"]})

    # Add edges: Kit holders to 0.0.0
    for kh_key, kh_value in kit_holders.items():
        for kh_content in kh_value["contents"]:
            if kh_content["position"] in matrix_dict and "0.0.0" in matrix_dict[kh_content["position"]]:
                filtered_matrix.append({"edge": f"({kh_content['position']}, 0.0.0)", "distance": matrix_dict[kh_content["position"]]["0.0.0"] + 2000})

    # Add edges: Gravity racks to specific kit holders
    for container_key, container_value in containers.items():
        for cont_content in container_value["contents"]:
            for kh_key, kh_value in kit_holders.items():
                for kh_content in kh_value["contents"]:
                    if kh_content["type"] == cont_content["type"]:
                        if cont_content["position"] in matrix_dict and kh_content["position"] in matrix_dict[cont_content["position"]]:
                            filtered_matrix.append({"edge": f"({cont_content['position']}, {kh_content['position']})",
                                                    "distance": matrix_dict[cont_content["position"]][kh_content["position"]] + 2000})

    # Add edges: Kit holders to all gravity racks
    for kh_key, kh_value in kit_holders.items():
        for kh_content in kh_value["contents"]:
            if kh_content["position"] in matrix_dict:
                for target, distance in matrix_dict[kh_content["position"]].items():
                    if target.startswith("1.") or target.startswith("2."):
                        filtered_matrix.append({"edge": f"({kh_content['position']}, {target})", "distance": distance + 2000})

    return filtered_matrix

def randomize_containers(containers_template):
    all_components = []
    for container in containers_template.values():
        for content in container["contents"]:
            if content["type"] not in all_components:
                all_components.append(content["type"])

    random.shuffle(all_components)

    new_containers = {}
    for idx, container_key in enumerate(containers_template.keys(), start=1):
        group = 1 if idx <= 7 else 2
        subgroup = idx if group == 1 else idx - 7
        gr_position = f"{group}.{subgroup}"

        component_type = all_components[(idx - 1) % len(all_components)]
        new_contents = [
            {"position": f"{gr_position}.{i}", "type": component_type}
            for i in range(1, 5)
        ]

        new_containers[container_key] = {"gr_position": gr_position, "contents": new_contents}

    return new_containers

def filter_distance_matrix(matrix, random_config):
    filtered_matrix = []
    containers = random_config["containers"]
    kit_holders = random_config["kit_holders"]

    # Transform distance matrix to a lookup dictionary
    matrix_dict = {}
    for entry in matrix:
        edge = entry["edge"].strip("()").split(", ")
        source, target = edge[0], edge[1]
        if source not in matrix_dict:
            matrix_dict[source] = {}
        matrix_dict[source][target] = entry["distance"]

    # Add edges: 0.0 to all gravity racks
    if "0.0" in matrix_dict:
        for target, distance in matrix_dict["0.0"].items():
            filtered_matrix.append({"edge": f"(0.0, {target})", "distance": distance + 2000})

    # Add edges: 0.0.0 to 0.0
    if "0.0.0" in matrix_dict and "0.0" in matrix_dict["0.0.0"]:
        filtered_matrix.append({"edge": "(0.0.0, 0.0)", "distance": matrix_dict["0.0.0"]["0.0"]})

    # Add edges: Kit holders to 0.0.0
    for kh_key, kh_value in kit_holders.items():
        for kh_content in kh_value["contents"]:
            if kh_content["position"] in matrix_dict and "0.0.0" in matrix_dict[kh_content["position"]]:
                filtered_matrix.append({"edge": f"({kh_content['position']}, 0.0.0)", "distance": matrix_dict[kh_content["position"]]["0.0.0"] + 2000})

    # Add edges: Gravity racks to specific kit holders
    for container_key, container_value in containers.items():
        for cont_content in container_value["contents"]:
            for kh_key, kh_value in kit_holders.items():
                for kh_content in kh_value["contents"]:
                    if kh_content["type"] == cont_content["type"]:
                        if cont_content["position"] in matrix_dict and kh_content["position"] in matrix_dict[cont_content["position"]]:
                            filtered_matrix.append({"edge": f"({cont_content['position']}, {kh_content['position']})",
                                                    "distance": matrix_dict[cont_content["position"]][kh_content["position"]] + 2000})

    # Add edges: Kit holders to all gravity racks
    for kh_key, kh_value in kit_holders.items():
        for kh_content in kh_value["contents"]:
            if kh_content["position"] in matrix_dict:
                for target, distance in matrix_dict[kh_content["position"]].items():
                    if target.startswith("1.") or target.startswith("2."):
                        filtered_matrix.append({"edge": f"({kh_content['position']}, {target})", "distance": distance + 2000})

    return filtered_matrix

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

def containers_from_gr_sequence(gr_seq, containers_template):
    """
    Turns [{"1.1": "Container_1"}, …] into the classic
    {"Container_1": {"gr_position": "1.1", "contents": …}, …}
    """
    import copy
    cfg = {}
    for mapping in gr_seq:
        pos, cid = next(iter(mapping.items()))
        if cid not in containers_template:
            raise KeyError(f"{cid} absent from containers_template")
        c = copy.deepcopy(containers_template[cid])
        c["gr_position"] = pos
        for i, comp in enumerate(c["contents"], start=1):
            comp["position"] = f"{pos}.{i}"
        cfg[cid] = c
    return cfg

def generate_unique_gr_configurations(num_configs, containers_template):
    configurations = {}
    while len(configurations) < num_configs:
        config = randomize_containers(containers_template)
        key = "-".join(f"{container['gr_position']}:{content['type']}" for container in config.values() for content in
                       container["contents"])
        if key not in configurations:
            configurations[key] = config
    return configurations

def gr_sequence_from_containers(containers_dict):
    """
    Turn {'Container_1': {'gr_position': '1.1', …}, …}
    →  [ {'1.1': 'Container_1'}, {'1.2': 'Container_2'}, … ]
    Positions are sorted row-major (row.column as ints).
    """
    tmp = [(meta["gr_position"], cid) for cid, meta in containers_dict.items()]

    def sort_key(item):
        row, col = map(int, item[0].split('.'))
        return (row, col)

    return [{pos: cid} for pos, cid in sorted(tmp, key=sort_key)]

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

def shuffle_container_positions(containers_dict):
    """
    Returns a *new* dict where each container ID keeps its own contents
    but is assigned a random, unique GR position.
    """
    import copy, random
    shuffled = copy.deepcopy(containers_dict)

    # Take the existing list of positions (['1.1', '1.2', …, '2.7'])
    positions = [meta["gr_position"] for meta in shuffled.values()]
    random.shuffle(positions)

    for (cid, meta), new_pos in zip(shuffled.items(), positions):
        meta["gr_position"] = new_pos
        # update the four inner slot co-ordinates
        for i, comp in enumerate(meta["contents"], 1):
            comp["position"] = f"{new_pos}.{i}"
    return shuffled

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
