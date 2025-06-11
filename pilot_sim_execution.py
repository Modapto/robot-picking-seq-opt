import json
import copy
from time import time
from pilot_sim_preprocessing import *

def convert_to_native_types(data):
    if isinstance(data, dict):
        return {k: convert_to_native_types(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_to_native_types(v) for v in data]
    elif isinstance(data, (int, float, str, bool)) or data is None:
        return data
    return str(data)

def run_simulation(input_data=None):
    total_time_start = int(time() * 1000)

    # ──────────────────────── 1 · INPUT ────────────────────────
    if input_data and "data" in input_data:
        print("Remote input data received.")
        data = input_data["data"]

        data["kh_sequences"] = normalise_kh_sequences(data.get("kh_sequences", []))
        if "gr_sequence" in data:                       # new style
            current_containers = containers_from_gr_sequence(
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

    baseline_gr_sequence = gr_sequence_from_containers(current_containers)

    print("\n>>> Finding Best Configuration for Full Sequence...")
    best_total_value = float("inf")
    runs = []

    for run_id in range(num_random_gr_configs):
        print(f"\n>>> Run {run_id + 1} with GR Configuration...")

        gr_config = shuffle_container_positions(current_containers)
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
            "gr_sequence": gr_sequence_from_containers(gr_config),
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
    with open("pilot_sim_execution_output.json", "w") as f:
        json.dump(output_data, f, indent=4)

    print("Simulation completed and results saved.")
    return output_data



