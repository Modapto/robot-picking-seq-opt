# dual_sim_execution.py
import json
import time
import random

from parse_json_dual import create_distance_matrices
from GraphCreation_dual import create_directed_bipartite_graph
from dual_gripper_heuristic import nearest_tsp_dual
from linear_dual import linear_picking_dual

# import helper functions & config from your optimization main
from main_dual import (
    build_edges_from_input,
    check_rules,
    generate_kh_nodes,
    build_time_details_from_tour,
)

# GR shuffle helpers
from dual_sim_GR import shuffle_container_positions, apply_gr_sequence_to_data
# If in the future you also want to shuffle KH, you can bring in:
# from dual_sim_KH import apply_kh_sequences_to_data


def compute_path_cost(G, tour):
    cost = 0
    for u, v in zip(tour, tour[1:]):
        if not G.has_edge(u, v):
            raise ValueError(f"No edge {u} -> {v} in graph.")
        cost += int(G[u][v]["weight"])
    return cost


def _build_graph_bundle(data, require_type_match_gr_kh, allow_cross_rack=True, use_prune=True):
    """
    Build edges/matrix/graph under a chosen GR→KH policy.
    - require_type_match_gr_kh=True  : only GR→KH where types match (heuristic)
    - require_type_match_gr_kh=False : GR→KH for ALL pairs (linear baseline)
    Returns: (edges, gr_types, kh_types, B, set_kh, set_gr)
    """
    edges, gr_nodes, kh_nodes = build_edges_from_input(
        data,
        use_prune=use_prune,
        require_type_match_gr_kh=require_type_match_gr_kh,
    )

    # Optional diagnostics
    violations = check_rules(
        edges, gr_nodes, kh_nodes,
        allow_cross_rack_gr_pick2=allow_cross_rack,
        require_type_match_gr_kh=require_type_match_gr_kh,
    )
    if violations:
        hdr = "RULE CHECKS FAILED (GR→KH type relaxed)" if not require_type_match_gr_kh else "RULE CHECKS FAILED"
        print(hdr + f": {len(violations)} issues (continuing).")

    a_to_b = create_distance_matrices({"data": {"distance_matrix": edges}})

    # Active KH slots: axis for bipartite creation
    templates = data.get("templates", {})
    kit_holders_tpl = templates.get("kit_holders_opt", data.get("kit_holders_opt", {}))
    kh_seq = templates.get("kh_sequences_opt", data.get("kh_sequences_opt", []))
    kh_nodes_again = generate_kh_nodes(kh_seq, kit_holders_tpl)
    active_kh_nodes = sorted(kh_nodes_again.keys())

    # Sanity
    missing = [n for n in active_kh_nodes if n not in a_to_b.index or n not in a_to_b.columns]
    if missing:
        raise ValueError(f"KH nodes not in matrix: {missing}")

    B, set_1, set_2 = create_directed_bipartite_graph(a_to_b, active_kh_nodes)

    return edges, gr_nodes, kh_nodes, B, set_1, set_2


def evaluate_dual_methods(data, allow_cross_rack=True, use_prune=True):
    """
    Evaluate both methods on the SAME input:
      - dual_heuristic : strict GR→KH type matching
      - linear_dual    : relaxed GR→KH (all pairs)
    Returns dict with both costs, tours and time_details.
    """
    start_node = "0.0"
    end_node = "0.0.0"

    # Heuristic bundle (STRICT GR→KH type matching)
    (edges_strict,
     gr_types_strict, kh_types_strict,
     B_strict, set_kh_strict, set_gr_strict) = _build_graph_bundle(
        data,
        require_type_match_gr_kh=True,
        allow_cross_rack=allow_cross_rack,
        use_prune=use_prune,
    )

    tour_h = nearest_tsp_dual(
        G=B_strict,
        start=start_node,
        end=end_node,
        set_kh=set_kh_strict,
        set_gr=set_gr_strict,
        gr_types=gr_types_strict,
        kh_types=kh_types_strict,
        max_load=2,
        verbose=False,
    )
    cost_h = compute_path_cost(B_strict, tour_h)
    time_details_h = build_time_details_from_tour(B_strict, tour_h, gr_types_strict, kh_types_strict)

    # Linear bundle (RELAXED GR→KH type matching — this removes the error you saw)
    (edges_relaxed,
     gr_types_relaxed, kh_types_relaxed,
     B_relaxed, set_kh_relaxed, set_gr_relaxed) = _build_graph_bundle(
        data,
        require_type_match_gr_kh=False,
        allow_cross_rack=allow_cross_rack,
        use_prune=use_prune,
    )

    lin = linear_picking_dual(
        B=B_relaxed,
        start_node=start_node,
        end_node=end_node,
        set_kh=set_kh_relaxed,
        set_gr=set_gr_relaxed,
        gr_types=gr_types_relaxed,
        kh_types=kh_types_relaxed,
        filtered_matrix=edges_relaxed,  # use same weights
    )
    tour_l = lin["tour"]
    cost_l = lin.get("total_cost", compute_path_cost(B_relaxed, tour_l))
    time_details_l = build_time_details_from_tour(B_relaxed, tour_l, gr_types_relaxed, kh_types_relaxed)

    return {
        "dual_heuristic": {
            "cost": cost_h,
            "tour": tour_h,
            "time_details": time_details_h,
        },
        "linear_dual": {
            "cost": cost_l,
            "tour": tour_l,
            "time_details": time_details_l,
        },
    }


def run_dual_simulation(
    json_path="input_dual_gripper_sim.json",
    num_trials=25,
    shuffle_strategy="shuffle",
    seed=42,
    output_path="dual_sim_execution_output.json",
    allow_cross_rack=True,
    use_prune=True,
):
    """
    1) Evaluate baseline (current gr_sequence) with both methods.
    2) Generate 'num_trials' alternative GR layouts by shuffling containers.
    3) Keep the best improvement vs. baseline for the heuristic (and report linear too).
    4) Save a compact JSON result similar to your single-gripper co-sim output.
    """
    t0 = int(time.time() * 1000)

    with open(json_path) as f:
        msg = json.load(f)
    data = msg.get("data", msg)

    # Baseline evaluation (strict for heuristic, relaxed for linear)
    base = evaluate_dual_methods(data, allow_cross_rack=allow_cross_rack, use_prune=use_prune)
    base_h = base["dual_heuristic"]["cost"]
    base_l = base["linear_dual"]["cost"]

    baseline = {
        "dual_heuristic": {"cost": str(base_h)},
        "linear_dual": {"cost": str(base_l)},
        "gr_sequence": data.get("gr_sequence", []),
    }

    best = {
        "phase": None,
        "dual_heuristic_cost": str(base_h),
        "improvement_heuristic": 0.0,
        "improvement_linear": 0.0,
        "gr_sequence": baseline["gr_sequence"],
        "results": None,  # optional full tours/time_details for inspection
    }

    for phase in range(1, num_trials + 1):
        trial_seed = (seed + phase) if seed is not None else None
        new_seq = shuffle_container_positions(
            data.get("gr_sequence", []),
            seed=trial_seed,
            strategy=shuffle_strategy,
        )
        trial_data = apply_gr_sequence_to_data(data, new_seq)

        res = evaluate_dual_methods(trial_data, allow_cross_rack=allow_cross_rack, use_prune=use_prune)
        c_h = res["dual_heuristic"]["cost"]
        c_l = res["linear_dual"]["cost"]

        imp_h = round(((base_h - c_h) / base_h) * 100, 4) if base_h else 0.0
        imp_l = round(((base_l - c_l) / base_l) * 100, 4) if base_l else 0.0

        if imp_h > best["improvement_heuristic"]:
            best.update({
                "phase": phase,
                "dual_heuristic_cost": str(c_h),
                "improvement_heuristic": imp_h,
                "improvement_linear": imp_l,
                "gr_sequence": new_seq,
                "results": res,
            })

    out = {
        "simulation_run": True,
        "message": ("Improved GR configuration found." if best["phase"] else "No better layout than baseline."),
        "baseline": baseline,
        "best_phase": {
            "phase": best["phase"],
            "dual_heuristic_cost": best["dual_heuristic_cost"],
            "improvement_heuristic": best["improvement_heuristic"],
            "improvement_linear": best["improvement_linear"],
            "gr_sequence": best["gr_sequence"],
        },
        "solutionTime": int(time.time() * 1000) - t0,
        "totalTime": int(time.time() * 1000) - t0,
    }

    with open(output_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"✅ Wrote {output_path}")
    return out


if __name__ == "__main__":
    # tweak params as you like
    run_dual_simulation()
