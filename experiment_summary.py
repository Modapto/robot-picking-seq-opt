import os
import pandas as pd

base_dir = "Experiment Results Symmetric"

structured_data = []

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.startswith('results_') and file.endswith('.csv'):
            #path to the CSV file
            file_path = os.path.join(root, file)

            df = pd.read_csv(file_path)

            #Extract unique Gravity Rack and Kit Holder from the first row
            gravity_rack = df['Gravity Rack'].iloc[0]
            kit_holder = df['Kit Holder'].iloc[0]
            ratio = f"{gravity_rack} : {kit_holder}"

            #Process each run for the given file
            for run_id in df['Run'].unique():
                run_data = df[df['Run'] == run_id]

                result_row = {
                    'Gravity Rack': gravity_rack,
                    'Kit Holder': kit_holder,
                    'Ratio Gravity Rack: Kit Holder': ratio,
                    'Run': run_id
                }

                #Extract data for each method
                for method in ['Exact', 'Nearest', '2-opt', 'Q-learning']:
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

final_summary_df = pd.DataFrame(structured_data)

#Save the summary as an Excel file
summary_excel_file = os.path.join(base_dir, "Experiment Summary Symmetric.xlsx")
final_summary_df.to_excel(summary_excel_file, index=False)

print(f"Complete summary saved to {summary_excel_file}")


