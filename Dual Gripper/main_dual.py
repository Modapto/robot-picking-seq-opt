# dual_main.py
import json
import sys

import dual_optimization as opt
import dual_simulation as sim

DEFAULT_JSON = "input_dual.json"

ALLOWED_OPT_METHODS = {"heuristic", "linear", "heuristic-linear"}
SIMULATION_METHOD = "simulation"


def run_from_msg(msg: dict):
    """
    Dispatch runner:
      - method == "simulation"           -> dual_simulation.run_dual_simulation(...)
      - method in {"heuristic","linear","heuristic-linear"}
                                         -> dual_optimization.run_dual_optimization(...)
    Both submodules are responsible for writing their own output files:
      - dual_optimization_output.json
      - dual_simulation_output.json
    """
    data = msg.get("data", msg)
    method = data.get("method", "heuristic")

    if method == SIMULATION_METHOD:
        runs = data.get("num_random_gr_configs", 10)
        print(f"→ Running simulation with {runs} randomized GR layouts…")
        return sim.run_dual_simulation(input_data={"data": data})

    if method in ALLOWED_OPT_METHODS:
        print(f"→ Running optimization with method='{method}'…")
        return opt.run_dual_optimization(input_data={"data": data})

    raise ValueError(
        f"Unknown method '{method}'. "
        f"Use one of: {sorted(ALLOWED_OPT_METHODS | {SIMULATION_METHOD})}"
    )


def main():
    if len(sys.argv) < 2:
        json_path = DEFAULT_JSON
        print(f"(no arg given) → using default JSON: {json_path}")
        with open(json_path, "r") as f:
            msg = json.load(f)
        run_from_msg(msg)
    else:
        json_path = sys.argv[1]
        with open(json_path, "r") as f:
            msg = json.load(f)
        run_from_msg(msg)


if __name__ == "__main__":
    main()
