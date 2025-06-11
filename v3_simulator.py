import json
import copy
from time import time
from configurations_final import (
    load_distance_matrix,
    load_containers_template,
    load_kit_holders_template,
    randomize_containers,
    filter_distance_matrix
)
from exact_method import run_exact_tsp
from method_linear import linear_picking, total_cost
from GraphCreation import create_directed_bipartite_graph
from parse_json import create_distance_matrices

# ------------------------------------------------------------------
# === Backwards-compat / new-format adapter ========================
def _normalise_kh_sequences(raw_seqs):
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


def _containers_from_gr_sequence(gr_seq, containers_template):
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
# ------------------------------------------------------------------


def generate_unique_gr_configurations(num_configs, containers_template):
    configurations = {}
    while len(configurations) < num_configs:
        config = randomize_containers(containers_template)
        key = "-".join(f"{container['gr_position']}:{content['type']}" for container in config.values() for content in
                       container["contents"])
        if key not in configurations:
            configurations[key] = config
    return configurations

# ------------------------------------------------------------------
def _gr_sequence_from_containers(containers_dict):
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
# ------------------------------------------------------------------


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

# ------------------------------------------------------------------
def _shuffle_container_positions(containers_dict):
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
# ------------------------------------------------------------------
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


def run_simulation(input_data=None):
    total_time_start = int(time() * 1000)

    # ──────────────────────── 1 · INPUT ────────────────────────
    if input_data and "data" in input_data:
        print("Remote input data received.")
        data = input_data["data"]

        data["kh_sequences"] = _normalise_kh_sequences(data.get("kh_sequences", []))
        if "gr_sequence" in data:                       # new style
            current_containers = _containers_from_gr_sequence(
                data["gr_sequence"], data["containers_template"]
            )
        else:                                           # legacy style
            current_containers = data["current_config"]["containers"]

        distance_matrix       = data.get("distance_matrix")
        containers_template   = data["containers_template"]
        kit_holders_template  = data["kit_holders_template"]
        kh_sequences          = data["kh_sequences"] or [data.get("kh_setup", [])]
        num_random_gr_configs = data["num_random_gr_configs"]
        uuid                  = input_data["uuid"]
    else:
        raise ValueError("Input data is required, either via JSON file or directly.")

    # ── helper: build KH node set from *generated* configs ───────────────
    def _build_kh_nodes(kh_sequences, template):
        nodes = set()
        for seq in kh_sequences:
            kh_cfg = generate_kh_configuration(seq, template)
            for kh in kh_cfg.values():
                nodes.add(kh["kh_position"])           # e.g. "4"
                for comp in kh["contents"]:
                    nodes.add(comp["position"])        # e.g. "4.3"
        return nodes

    kh_nodes = _build_kh_nodes(kh_sequences, kit_holders_template)

    def build_gr_nodes(c_dict):
        g = {}
        for meta in c_dict.values():
            for comp in meta["contents"]:
                g[comp["position"]] = comp["type"]
            g[meta["gr_position"]] = meta["contents"][0]["type"]
        return g

    gr_nodes_baseline = build_gr_nodes(current_containers)

    print("\n>>> Computing Baseline for Full Sequence...")
    baseline_conf = {
        "containers": current_containers,
        "kit_holders_template": kit_holders_template,
        "kh_sequences": kh_sequences,
    }

    bl_exact_cost, _, bl_exact_raw = calculate_full_sequence_cost(
        distance_matrix, baseline_conf, method="exact"
    )
    bl_linear_cost, _, bl_linear_raw = calculate_full_sequence_cost(
        distance_matrix, baseline_conf, method="linear"
    )

    bl_exact_det  = [annotate_component_in_time_details(seg, gr_nodes_baseline, kh_nodes)
                     for seg in bl_exact_raw]
    bl_linear_det = [annotate_component_in_time_details(seg, gr_nodes_baseline, kh_nodes)
                     for seg in bl_linear_raw]

    print(f"Baseline exact value:  {bl_exact_cost}")
    print(f"Baseline linear value: {bl_linear_cost}")

    baseline_gr_sequence = _gr_sequence_from_containers(current_containers)

    print("\n>>> Finding Best Configuration for Full Sequence...")
    best_total_value = float("inf")
    runs = []

    for run_id in range(num_random_gr_configs):
        print(f"\n>>> Run {run_id + 1} with GR Configuration...")

        gr_config = _shuffle_container_positions(current_containers)
        gr_nodes_phase = build_gr_nodes(gr_config)

        run_conf = {
            "containers": gr_config,
            "kit_holders_template": kit_holders_template,
            "kh_sequences": kh_sequences,
        }

        cost, _, seg_raw = calculate_full_sequence_cost(
            distance_matrix, run_conf, method="exact"
        )
        seg_det = [annotate_component_in_time_details(seg, gr_nodes_phase, kh_nodes)
                   for seg in seg_raw]

        imp_exact  = round((bl_exact_cost  - cost) / bl_exact_cost  * 100, 4)
        imp_linear = round((bl_linear_cost - cost) / bl_linear_cost * 100, 4)

        runs.append({
            "phase": run_id + 1,
            "exact_cost": cost,
            "time_details": seg_det,
            "improvement_exact":  imp_exact,
            "improvement_linear": imp_linear,
            "gr_sequence": _gr_sequence_from_containers(gr_config),
        })

        best_total_value = min(best_total_value, cost)

    end_time = int(time() * 1000)
    output_data = {
        "uuid": uuid,
        "produced_at": end_time,
        "data": {
            "baseline": {
                "exact":  {"cost": bl_exact_cost,  "time_details": bl_exact_det},
                "linear": {"cost": bl_linear_cost, "time_details": bl_linear_det},
                "gr_sequence": baseline_gr_sequence,
            },
            "phases": runs,
            "best_total_value": best_total_value,
            "solutionTime": end_time - total_time_start,
            "totalTime":    end_time - total_time_start,
        },
    }

    output_data = convert_to_native_types(output_data)
    with open("simulation_results_v2.json", "w") as f:
        json.dump(output_data, f, indent=4)

    print("Simulation completed and results saved.")
    return output_data


def convert_to_native_types(data):
    if isinstance(data, dict):
        return {k: convert_to_native_types(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_to_native_types(v) for v in data]
    elif isinstance(data, (int, float, str, bool)) or data is None:
        return data
    return str(data)

if __name__ == "__main__":
    with open("in.json", "r") as f:
        simulation_input = json.load(f)
    run_simulation(simulation_input)


