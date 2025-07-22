import json, pickle, base64
from time import time
from pilot_co_sim_KH import normalise_kh_sequences, generate_kh_configuration, annotate_component_in_time_details, calculate_full_sequence_cost
from pilot_co_sim_GR import containers_from_gr_sequence, gr_sequence_from_containers, shuffle_container_positions, filter_distance_matrix

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
    all_phases  = []
    best_phase  = None
    best_cost   = float("inf")

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

        phase_dict = {
            "phase": run_id + 1,
            "exact_cost": cost,
            # "time_details": seg_det,
            "improvement_exact":  imp_exact,
            "improvement_linear": imp_linear,
            "gr_sequence": gr_sequence_from_containers(gr_config),
        }
        all_phases.append(phase_dict)

        # keep only phases that beat BOTH baselines
        if cost < bl_exact_cost and cost < bl_linear_cost and cost < best_cost:
            best_cost  = cost
            best_phase = phase_dict
    success = best_phase is not None
    end_time = int(time() * 1000)

    output_data = {
            "simulation_run": success,
            "message": ("Improved GR configuration found."
                        if success else
                        "No GR configuration beat both baseline costs."),
            "baseline": {
                "exact":  {"cost": bl_exact_cost },   #,  "time_details": bl_exact_det
                "linear": {"cost": bl_linear_cost},   #, "time_details": bl_linear_det
                "gr_sequence": baseline_gr_sequence,
            },
            "best_phase": best_phase,  # null if no qualifying phase
            # "phases": all_phases,           # ← uncomment if you still want them
            "solutionTime": end_time - total_time_start,
            "totalTime": end_time - total_time_start,
    }

    # ── 4 · SAVE DECODED FILE ──────────────────────────────────────
    decoded_path = "pilot_sim_execution_output.json"
    with open(decoded_path, "w") as f_dec:
        json.dump(convert_to_native_types(output_data), f_dec, indent=4)
    print(f"Decoded result written to {decoded_path}")

    # ── 5 · SAVE ENCODED WRAPPER ───────────────────────────────────
    encoded_blob = base64.b64encode(pickle.dumps(output_data)).decode()
    wrapper = {
        "uuid": uuid,
        "produced_at": end_time,
        "data": {"base64": encoded_blob}
    }
    encoded_path = "encoded_sim_output.json"
    with open(encoded_path, "w") as f_enc:
        json.dump(wrapper, f_enc, indent=4)
    print(f"Encoded result written to {encoded_path}")

    print("Simulation completed and results saved.")
    return output_data



