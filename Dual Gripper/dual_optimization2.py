
# dual_optimization.py
import json, sys
from time import time

from dual_core import evaluate_methods_on_data

DEFAULT_JSON = "input_dual_gripper.json"
OUTPUT_PATH  = "dual_optimization_output.json"

USE_PRUNE = True
ADD_EDGE_BIAS = 2000
ALLOW_CROSS_RACK = True
CROSS_GR_EXTRA_BIAS = 0

def run_dual_optimization(json_file_path=None, input_data=None):
    t0 = int(time() * 1000)

    if input_data and "data" in input_data:
        data = input_data["data"]
    elif json_file_path:
        with open(json_file_path) as f:
            msg = json.load(f)
        data = msg.get("data", msg)
    else:
        raise ValueError("run_dual_optimization needs either json_file_path or input_data")

    method = data.get("method", "heuristic")
    if method not in ("heuristic", "linear", "heuristic-linear"):
        raise ValueError(f"Unsupported method '{method}' for optimization")

    eval_res = evaluate_methods_on_data(
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

    results = {}
    if method in ("heuristic", "heuristic-linear"):
        results["heuristic"] = eval_res["heuristic"]
    if method in ("linear", "heuristic-linear"):
        results["linear"] = eval_res["linear"]

    if method == "heuristic-linear":
        ch = results["heuristic"]["cost"]
        cl = results["linear"]["cost"]
        improvement = round(((cl - ch) / cl) * 100, 4) if cl else 0.0
        results["improvement_percentage"] = improvement

    out = {
        "message": f"Optimization ran with method='{method}'.",
        "solutionTime": int(time() * 1000) - t0,
        "optimization_results": results
    }
    with open(OUTPUT_PATH, "w") as f:
        json.dump(out, f, indent=2)
    print(f"✅ Wrote {OUTPUT_PATH}")
    return out

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"(no arg given) → using default JSON: {DEFAULT_JSON}")
        run_dual_optimization(json_file_path=DEFAULT_JSON)
    else:
        run_dual_optimization(json_file_path=sys.argv[1])
