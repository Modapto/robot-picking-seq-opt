import random
import copy
import json
from itertools import product
from time import time
from graph_creation import create_directed_bipartite_graph  # Assuming you have this function
from exact import run_exact_tsp  # Assuming the exact method is defined elsewhere
from linear_method import linear_picking  # Assuming the linear picking method is defined elsewhere
from configurations_with_extra_distance import randomize_containers, randomize_kit_holders, generate_all_kh_configurations, filter_distance_matrix

# Load the existing distance matrix
with open('final_distance_matrix.json', 'r') as f:
    distance_matrix = json.load(f)

# Constants for simulation
NUM_GR_CONFIGS = 10  # Number of gravity rack configurations to generate
NUM_KH_CONFIGS = 1  # Number of kit holder configurations to generate
OUTPUT_FILE = "simulation_results.json"

# Load container and kit holder templates
with open("containers_template.json", "r") as f:
    containers_template = json.load(f)

with open("kit_holders_template.json", "r") as f:
    kit_holders_template = json.load(f)
# Generate multiple GR configurations
def generate_gr_configurations(num_configs, containers_template):
    configurations = []
    for _ in range(num_configs):
        config = randomize_containers(containers_template)
        configurations.append(config)
    return configurations

# Generate multiple KH configurations
def generate_kh_configurations(num_configs, kit_holders_template):
    configurations = []
    all_kh_configs = generate_all_kh_configurations(kit_holders_template)
    for _ in range(num_configs):
        selected_config = random.choice(all_kh_configs)
        config = randomize_kit_holders(kit_holders_template, selected_config)
        configurations.append(config)
    return configurations

# Filter the distance matrix for a specific GR-KH pair
def filter_and_solve(gr_config, kh_config, method):
    # Create a combined configuration
    random_config = {"containers": gr_config, "kit_holders": kh_config}
    filtered_matrix = filter_distance_matrix(distance_matrix, random_config)

    # Create the bipartite graph
    B, set_1, set_2 = create_directed_bipartite_graph(filtered_matrix)

    # Solve using the selected method
    start_time = int(time() * 1000)
    if method == "exact":
        tour, cost, time_details = run_exact_tsp(filtered_matrix)
    elif method == "linear_picking":
        result = linear_picking(B, "0.0", "0.0.0", set_1, set_2)
        tour = result["tour"]
        cost = result["total_cost"]
        _, time_details = total_cost(B, tour)
    else:
        raise ValueError("Invalid method specified")

    end_time = int(time() * 1000)
    return {
        "method": method,
        "tour": tour,
        "cost": cost,
        "time_details": time_details,
        "solution_time": end_time - start_time,
    }

# Main simulation logic
def run_simulation(num_gr_configs, num_kh_configs, method):
    gr_configs = generate_gr_configurations(num_gr_configs, containers_template)
    kh_configs = generate_kh_configurations(num_kh_configs, kit_holders_template)
    results = []

    for gr_idx, gr_config in enumerate(gr_configs):
        for kh_idx, kh_config in enumerate(kh_configs):
            print(f"Processing GR Config {gr_idx + 1}/{num_gr_configs}, KH Config {kh_idx + 1}/{num_kh_configs}...")
            try:
                result = filter_and_solve(gr_config, kh_config, method)
                results.append({
                    "gr_config_index": gr_idx,
                    "kh_config_index": kh_idx,
                    "gr_config": gr_config,
                    "kh_config": kh_config,
                    "result": result,
                })
            except Exception as e:
                print(f"Error solving GR {gr_idx} and KH {kh_idx}: {e}")
    return results

# Run the simulation and save results
simulation_results = run_simulation(NUM_GR_CONFIGS, NUM_KH_CONFIGS, "linear_picking")
with open(OUTPUT_FILE, "w") as f:
    json.dump(simulation_results, f, indent=4)
print(f"Simulation results saved to {OUTPUT_FILE}")
