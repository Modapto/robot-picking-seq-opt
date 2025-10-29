import json, sys, random
from time import time

from dual_core import (
    evaluate_methods_on_data,
    shuffle_gr_sequence,
)

DEFAULT_JSON = "input_dual.json"
OUTPUT_PATH  = "dual_simulation_output.json"

USE_PRUNE = True
ADD_EDGE_BIAS = 2000
ALLOW_CROSS_RACK = True
CROSS_GR_EXTRA_BIAS = 0

def run_dual_simulation(json_file_path=None, input_data=None):
    t0 = int(time() * 1000)

    if input_data and "data" in input_data:
        data = input_data["data"]
    elif json_file_path:
        with open(json_file_path) as f:
            msg = json.load(f)
        data = msg.get("data", msg)
    else:
        raise ValueError("run_dual_simulation needs either json_file_path or input_data")

    num_trials = int(data.get("num_random_gr_configs", 10))
    seed = int(data.get("random_seed", 42))
    rng = random.Random(seed)

    base_eval = evaluate_methods_on_data(
        data,
        require_type_match_gr_kh=False,
        use_prune=USE_PRUNE,
        add_bias=ADD_EDGE_BIAS,
        allow_cross_rack=ALLOW_CROSS_RACK,
        cross_gr_extra_bias=CROSS_GR_EXTRA_BIAS,
        start_node="0.0",
        end_node="0.0.0",
        verbose=False
    )
    baseline = {
        "heuristic": base_eval["heuristic"],
        "linear": base_eval["linear"]
    }

    best = {
        "heuristic_cost": base_eval["heuristic"]["cost"],
        "linear_cost": base_eval["linear"]["cost"],
        "heuristic": base_eval["heuristic"],
        "linear": base_eval["linear"],
        "gr_sequence": data["gr_sequence"],
        "phase": 0
    }

    phases = []
    for k in range(num_trials):
        try_data = json.loads(json.dumps(data))
        try_data["gr_sequence"] = shuffle_gr_sequence(try_data["gr_sequence"], rng)

        ev = evaluate_methods_on_data(
            try_data,
            require_type_match_gr_kh=False,
            use_prune=USE_PRUNE,
            add_bias=ADD_EDGE_BIAS,
            allow_cross_rack=ALLOW_CROSS_RACK,
            cross_gr_extra_bias=CROSS_GR_EXTRA_BIAS,
            start_node="0.0",
            end_node="0.0.0",
            verbose=False
        )
        phases.append({
            "phase": k + 1,
            "heuristic": ev["heuristic"],
            "linear": ev["linear"],
            "gr_sequence": try_data["gr_sequence"]
        })

        if ev["heuristic"]["cost"] < best["heuristic_cost"]:
            best = {
                "heuristic_cost": ev["heuristic"]["cost"],
                "linear_cost": ev["linear"]["cost"],
                "heuristic": ev["heuristic"],
                "linear": ev["linear"],
                "gr_sequence": try_data["gr_sequence"],
                "phase": k + 1,
            }

    # ---- compute improvements vs baseline ----
    base_h_cost = baseline["heuristic"]["cost"]
    base_l_cost = baseline["linear"]["cost"]
    best_h_cost = best["heuristic"]["cost"]
    best_l_cost = best["linear"]["cost"]

    # guard against divide-by-zero (shouldn't happen unless cost==0)
    if base_h_cost:
        heuristic_improvement_pct = round(((base_h_cost - best_h_cost) / base_h_cost) * 100, 4)
    else:
        heuristic_improvement_pct = 0.0

    if base_l_cost:
        linear_improvement_pct = round(((base_l_cost - best_l_cost) / base_l_cost) * 100, 4)
    else:
        linear_improvement_pct = 0.0

    out = {
        "message": f"Simulation ran {num_trials} randomized GR layouts (seed={seed}).",
        "solutionTime": int(time() * 1000) - t0,
        "baseline": baseline,
        "best": {
            "phase": best["phase"],
            "heuristic": best["heuristic"],
            "linear": best["linear"],
            "gr_sequence": best["gr_sequence"],

        },
        # new: improvement stats
        "improvements": {
            "heuristic_improvement_pct": heuristic_improvement_pct,
            "linear_improvement_pct": linear_improvement_pct
        }
        # ,"phases": phases
    }
    with open(OUTPUT_PATH, "w") as f:
        json.dump(out, f, indent=2)
    print(f"✅ Wrote {OUTPUT_PATH}")
    return out

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"(no arg given) → using default JSON: {DEFAULT_JSON}")
        run_dual_simulation(json_file_path=DEFAULT_JSON)
    else:
        run_dual_simulation(json_file_path=sys.argv[1])
