import os
import json
import pandas as pd
from test_main2 import run_tsp
from test_instances_generator2 import generate_feasible_instance

# Define problem configurations for Gravity Rack and Kit Holder positions
gravity_rack_configs = [
    (1, 2, 5), # Example configuration: 1x2x4 = 8 positions
    (1, 2, 10),
    (1, 2, 15),
    (1, 2, 20),
    (1, 2, 15)
]

kit_holder_configs = [
    (2, 4)  # Example configuration: 2x2 = 4 positions
]

# Base directory for experiment results
base_dir = "Experiment Results v2"
os.makedirs(base_dir, exist_ok=True)

# Master summary list to gather all experiment results
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

        for run_id in range(1, 11):  # 10 runs
            print(
                f"Running experiment with Gravity Rack: {rows}x{cols}x{components}, Kit Holder: {kh}x{blocks}, Run: {run_id}")

            # Loop to ensure we get a feasible instance
            while True:
                # Generate a random JSON input with the specified dropout rate k
                input_json = generate_feasible_instance(gravity_rack_positions, kit_holder_positions, k=0.5)

                # Check feasibility based on the nearest method
                if input_json:
                    print("Feasible instance generated and verified!")
                    break  # Exit loop once a feasible instance is found
                else:
                    print("Infeasible instance detected, regenerating...")

            # Save the input JSON to a file
            file_name_prefix = f"GR_{rows}x{cols}x{components}_KH_{kh}x{blocks}_Run_{run_id}"
            run_dir = f"{config_dir}/Run_{run_id}"
            os.makedirs(run_dir, exist_ok=True)
            input_json_file = f"{run_dir}/input_{file_name_prefix}.json"
            with open(input_json_file, 'w') as f:
                json.dump(input_json, f, indent=4)

            # Run the TSP methods and save inputs/outputs
            output_json_file = f"{run_dir}/output_{file_name_prefix}.json"
            results = run_tsp(input_json_file, output_json_file, gravity_rack_positions, kit_holder_positions)

            # Fetch the exact cost for calculating the optimality gap
            exact_cost = results['exact']['cost'] if 'exact' in results else None

            # Collect results in a row-wise format for the summary
            result_rows = []

            for method in ['nearest', '2-opt', 'q-learning', 'exact']:
                if method in results:
                    # Calculate the optimality gap
                    if exact_cost and method != 'exact':
                        optimality_gap = round(((results[method]['cost'] - exact_cost) / exact_cost) * 100, 2)
                    else:
                        optimality_gap = None  # No gap for the exact method itself

                    # Add result to the master summary list
                    experiment_summary.append([
                        f"{rows}x{cols}x{components}",  # Gravity Rack Size
                        f"{kh}x{blocks}",  # Kit Holder Size
                        run_id,  # Run Number
                        method.capitalize(),  # Method Name
                        results[method]['cost'],  # Cost of the Method
                        round(results[method]['exec_time'], 4),  # Execution Time
                        optimality_gap  # Optimality Gap
                    ])

                    # Create a separate result for each method, with more explicit rows for this run
                    result_rows.append([
                        f"{rows}x{cols}x{components}",  # Gravity Rack Size
                        f"{kh}x{blocks}",  # Kit Holder Size
                        run_id,  # Run Number
                        method.capitalize(),  # Method Name
                        results[method]['cost'],  # Cost of the Method
                        round(results[method]['exec_time'], 4),  # Execution Time
                        optimality_gap  # Optimality Gap
                    ])

            # Convert results to DataFrame and save to CSV for each run
            df_results = pd.DataFrame(result_rows,
                                      columns=['Gravity Rack', 'Kit Holder', 'Run', 'Method', 'Cost', 'Exec time',
                                               'Optimality Gap (%)'])
            results_csv_file = f"{run_dir}/results_{file_name_prefix}.csv"
            df_results.to_csv(results_csv_file, index=False)

            print(f"Results for run {run_id} saved to {results_csv_file}")

# Save the master summary to a CSV file
summary_csv_file = f"{base_dir}/experiment_summary.csv"
df_summary = pd.DataFrame(experiment_summary,
                          columns=['Gravity Rack', 'Kit Holder', 'Run', 'Method', 'Cost', 'Exec time',
                                   'Optimality Gap (%)'])
df_summary.to_csv(summary_csv_file, index=False)
print(f"Experiment summary saved to {summary_csv_file}")
