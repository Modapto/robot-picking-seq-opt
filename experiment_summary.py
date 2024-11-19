import os
import pandas as pd

# Base directory for experiment results for sparse graph
base_dir = "Experiment Results testing"

# List to hold the structured data
structured_data = []

# Walk through all directories and files in the base directory
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.startswith('results_GR_1x2x5_') and file.endswith('.csv'):
            # Path to the CSV file
            file_path = os.path.join(root, file)

            # # Extract the dropout rate (k) from the directory name
            # try:
            #     k_value = None
            #     for part in root.split(os.sep):
            #         if part.startswith("k_"):
            #             k_value = float(part.split("_")[1])
            #             break
            #     if k_value is None:
            #         raise ValueError(f"DropoutRate (k) not found in directory structure: {root}")
            # except Exception as e:
            #     print(f"Error determining DropoutRate for file: {file_path} - {e}")
            #     continue

            # Read the CSV file into a DataFrame
            df = pd.read_csv(file_path)

            # Extract unique Gravity Rack and Kit Holder from the first row
            gravity_rack = df['Gravity Rack'].iloc[0]
            kit_holder = df['Kit Holder'].iloc[0]
            ratio = f"{gravity_rack} : {kit_holder}"

            # Process each run for the given file
            for run_id in df['Run'].unique():
                run_data = df[df['Run'] == run_id]

                result_row = {
                    # 'DropoutRate': k_value,  # Add the dropout rate to the summary
                    'Gravity Rack': gravity_rack,
                    'Kit Holder': kit_holder,
                    'Ratio Gravity Rack: Kit Holder': ratio,
                    'Run': run_id
                }

                # Extract data for each method
                for method in ['Exact', 'Nearest', '2-opt', 'Q-learning', 'Ql-nearest', 'Ql-2-opt']:
                    method_data = run_data[run_data['Method'] == method]
                    if not method_data.empty:
                        result_row[f'Exec time {method}'] = method_data['Exec time'].values[0]
                        result_row[f'Cost {method}'] = method_data['Cost'].values[0]
                        result_row[f'Optimality Gap {method} (%)'] = method_data['Optimality Gap (%)'].values[0]
                    else:
                        result_row[f'Exec time {method}'] = None
                        result_row[f'Cost {method}'] = None
                        result_row[f'Optimality Gap {method} (%)'] = None

                structured_data.append(result_row)

# Convert the structured data into a DataFrame
final_summary_df = pd.DataFrame(structured_data)

# Save the summary as an Excel file
summary_excel_file = os.path.join(base_dir, "Experiment Summary testing10x10.xlsx")
final_summary_df.to_excel(summary_excel_file, index=False)

print(f"Complete summary saved to {summary_excel_file}")
