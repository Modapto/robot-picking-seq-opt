import random
import copy
import json
from configurations_final import *

# Load the existing distance matrix
with open('final_distance_matrix.json', 'r') as f:
    distance_matrix = json.load(f)

# Constants for simulation
NUM_GR_CONFIGS = 10  # Number of gravity rack configurations to generate
NUM_KH_CONFIGS = 5  # Number of kit holder configurations to generate
OUTPUT_FILE = "simulation_results.json"

# Load container and kit holder templates
with open("containers_template.json", "r") as f:
    containers_template = json.load(f)

with open("kit_holders_template.json", "r") as f:
    kit_holders_template = json.load(f)

# Generate multiple GR configurations
def generate_gr_configurations(num_configs, containers_template):
    """
    Generates multiple random configurations for gravity racks (GR).

    Parameters:
    - num_configs (int): Number of GR configurations to generate.
    - containers_template (dict): Template for containers.

    Returns:
    - List of GR configurations.
    """
    configurations = []
    for _ in range(num_configs):
        config = randomize_containers(containers_template)
        configurations.append(config)
    return configurations

# Generate multiple KH configurations
def generate_kh_configurations(num_configs, kit_holders_template):
    """
    Generates multiple random configurations for kit holders (KH).

    Parameters:
    - num_configs (int): Number of KH configurations to generate.
    - kit_holders_template (dict): Template for kit holders.

    Returns:
    - List of KH configurations.
    """
    configurations = []
    all_kh_configs = generate_all_kh_configurations(kit_holders_template)
    for _ in range(num_configs):
        selected_config = random.choice(all_kh_configs)
        config = randomize_kit_holders(kit_holders_template, selected_config)
        configurations.append(config)
    return configurations



