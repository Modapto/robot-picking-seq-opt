import json
import sys
import os
import tempfile
import shutil

# These are the two modules you already have
import dual_optimization as opt
import dual_simulation as sim


DEFAULT_INPUT = "input_dual_gripper.json"

ALLOWED_METHODS = {"simulation", "heuristic", "linear", "heuristic-linear"}


def _write_temp_input(msg: dict) -> str:
    """
    Write the provided message (with 'data' root) to a temporary JSON file and
    return its path. We'll point the optimization/simulation modules at this file.
    """
    tmpdir = tempfile.mkdtemp(prefix="dual_main_")
    path = os.path.join(tmpdir, "input_dual_gripper.json")
    with open(path, "w") as f:
        json.dump(msg, f, indent=2)
    return path


def run_from_msg(msg: dict):
    """
    Dispatch based on data.method:
      - simulation       -> dual_simulation.main()
      - heuristic        -> dual_optimization.main()
      - linear           -> dual_optimization.main()
      - heuristic-linear -> dual_optimization.main()
    We do NOT modify your other modules; we just point them to a temp input file
    and (for simulation) override N_PHASES if the user provided num_random_gr_configs.
    """
    if "data" not in msg:
        raise ValueError("Input must contain a 'data' object at the top level.")
    data = msg["data"]

    method = data.get("method", "heuristic")
    if method not in ALLOWED_METHODS:
        raise ValueError(f"Unknown method '{method}'. Allowed: {sorted(ALLOWED_METHODS)}")

    # Write a temp input so the submodules read exactly this payload
    temp_input_path = _write_temp_input(msg)

    try:
        if method == "simulation":
            # Allow the user to control the number of randomized GR layouts
            n = data.get("num_random_gr_configs")
            if isinstance(n, int) and n > 0:
                sim.N_PHASES = n  # override the module-level default

            # Point the simulation module at our temp file and run
            sim.INPUT_PATH = temp_input_path
            print(f"→ Running simulation with {sim.N_PHASES} randomized GR layouts…")
            sim.main()
            # Output is written by dual_simulation.py to dual_simulation_output.json

        else:
            # For optimization methods, just forward to the optimization module
            # The module already supports: 'heuristic', 'linear', 'heuristic-linear'
            opt.INPUT_PATH = temp_input_path
            print(f"→ Running optimization with method='{method}'…")
            opt.main()
            # Output is written by dual_optimization.py to dual_optimization_output.json

    finally:
        # Clean up the temp directory
        try:
            base_tmpdir = os.path.dirname(temp_input_path)
            shutil.rmtree(base_tmpdir, ignore_errors=True)
        except Exception:
            pass


def main():
    # Accept either: (a) path to an input JSON, or (b) no args -> DEFAULT_INPUT
    if len(sys.argv) > 1:
        in_path = sys.argv[1]
    else:
        in_path = DEFAULT_INPUT
        print(f"(no arg given) → using default JSON: {in_path}")

    with open(in_path, "r") as f:
        msg = json.load(f)

    # Dispatch to the appropriate runner
    run_from_msg(msg)


if __name__ == "__main__":
    main()
