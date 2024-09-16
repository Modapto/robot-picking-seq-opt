from Test_main import *
import os
import pandas as pd

# Define the problem configurations
gravity_rack_configs = [
    # Gravity Rack Test with KH 4x5 case
    (1, 2, 10),  # 1x2x10 = 20
    # (2, 2, 10),  # 2x2x10 = 40
    # (5, 2, 10),  # 5x2x10 = 100
    # (10, 2, 10),  # 10x2x10 = 200
    # (20, 2, 10),  # 20x2x10 = 400
    # (50, 2, 10),  # 50x2x10 = 1000
    # (100, 2, 10)  # 20x2x10 = 2000

    # # Gravity Rack Test with KH 4x25 case
    # (5, 2, 10),  # 5x2x10 = 100
    # (10, 2, 10),  # 10x2x10 = 200
    # (25, 2, 10),  # 25x2x10 = 500
    # (50, 2, 10),  # 50x2x10 = 1000
    # (100, 2, 10),  # 20x2x10 = 2000
    # (250, 2, 10),  # 250x2x10 = 5000
    # (500, 2, 10)  # 500x2x10 = 10000

    # Symmetric Instances
    # (2, 2, 10)  # 2x2x10 = 40
    # (5, 2, 10)  # 5x2x10 = 100
    # (10, 2, 10)  # 10x2x10 = 200
    # (15, 2, 10)  # 15x2x10 = 300
    # (20, 2, 10)  # 20x2x10 = 400
    # (25, 2, 10) # 25x2x10 = 500



]

kit_holder_configs = [
    (4, 5)  # 4x5 = 20
    # (4, 25)  # 4x25 = 100

    # Symmetric Instances
    # (4, 10) # 2x2x10 = 40
    # (4, 25)  # 4x25 = 100
    # (4, 50) # 4x50 = 200
    # (4, 75) # 4x75 = 300
    # (4, 100) # 4x100 = 400
    # (4, 125) # 4x125 = 500
]

# Base directory for experiment results
base_dir = "Experiment Results v2"
os.makedirs(base_dir, exist_ok=True)

# Master summary list to gather all experiments results
experiment_summary = []

# Run experiments and save results
for (rows, cols, components) in gravity_rack_configs:
    gravity_rack_positions = [f"{row}.{col}.{comp}" for row in range(1, rows + 1) for col in range(1, cols + 1) for comp
                              in range(1, components + 1)]

    for (kh, blocks) in kit_holder_configs:
        kit_holder_positions = [f"{kh}.{block}" for kh in range(1, kh + 1) for block in range(1, blocks + 1)]

        # Directory for this specific gravity rack and kit holder configuration
        config_dir = f"{base_dir}/GR_{rows}x{cols}x{components}_KH_{kh}x{blocks}"
        os.makedirs(config_dir, exist_ok=True)

        for run_id in range(1, 6):  # 5 runs
            print(
                f"Running experiment with Gravity Rack: {rows}x{cols}x{components}, Kit Holder: {kh}x{blocks}, Run: {run_id}")

            # Create a directory for this specific run
            run_dir = f"{config_dir}/Run_{run_id}"
            os.makedirs(run_dir, exist_ok=True)

            # File naming format
            file_name_prefix = f"GR_{rows}x{cols}x{components}_KH_{kh}x{blocks}_Run_{run_id}"

            # Generate the random JSON input
            input_json = generate_random_json_input(gravity_rack_positions, kit_holder_positions,
                                                    method="all")  # Use "all" to ensure the input works for all methods

            # Save the input JSON to a file
            input_json_file = f"{run_dir}/input_{file_name_prefix}.json"
            with open(input_json_file, 'w') as f:
                json.dump(input_json, f, indent=4)

            # Run the TSP methods and save inputs/outputs
            output_json_file = f"{run_dir}/output_{file_name_prefix}.json"

            # Run TSP for all methods
            results = run_tsp_for_size(input_json_file, output_json_file, gravity_rack_positions, kit_holder_positions)


            # Fetch the exact cost for calculating the optimality gap
            exact_cost = results['exact']['cost'] if 'exact' in results else None

            # Save the results in a row-wise format and collect summary for the master file
            result_rows = []  # Prepare rows for each method separately
            for method in ['nearest', '2-opt', 'q-learning', 'exact']:
                if method in results:
                    # Calculate the optimality gap
                    if exact_cost and method != 'exact':
                        optimality_gap = round(((results[method]['cost'] - exact_cost) / exact_cost) * 100,2)
                    else:
                        optimality_gap = None  # No gap for the exact method itself

                    # Add result to the master summary list
                    experiment_summary.append([
                        f"{rows}x{cols}x{components}",  # Gravity Rack Size
                        f"{kh}x{blocks}",               # Kit Holder Size
                        run_id,                         # Run Number
                        method.capitalize(),            # Method Name
                        results[method]['cost'],        # Cost of the Method
                        round(results[method]['exec_time'],4),   # Execution Time
                        optimality_gap                  # Optimality Gap
                    ])

                    # Create a separate result for each method, with more explicit rows for this run
                    result_rows.append([
                        f"{rows}x{cols}x{components}",  # Gravity Rack Size
                        f"{kh}x{blocks}",               # Kit Holder Size
                        run_id,                         # Run Number
                        method.capitalize(),            # Method Name
                        results[method]['cost'],        # Cost of the Method
                        round(results[method]['exec_time'],4),   # Execution Time
                        optimality_gap                  # Optimality Gap
                    ])

            # Convert result_rows to DataFrame directly for this run
            df_results = pd.DataFrame(result_rows, columns=[
                'Gravity Rack', 'Kit Holder', 'Run', 'Method', 'Cost', 'Exec time', 'Optimality Gap (%)'
            ])

            # Save the run-specific results to a CSV file
            results_csv_file = f"{run_dir}/results_{file_name_prefix}.csv"
            df_results.to_csv(results_csv_file, index=False)

            print(f"Results and files for run {run_id} saved to {run_dir}")


df_summary = pd.DataFrame(experiment_summary, columns=[
    'Gravity Rack', 'Kit Holder', 'Run', 'Method', 'Cost', 'Exec time', 'Optimality Gap (%)'
])
