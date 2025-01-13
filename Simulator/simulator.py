import json
import copy
from configurations_final import randomize_containers, filter_distance_matrix
from exact_method import run_exact_tsp
import pandas as pd
import numpy as np

def generate_unique_gr_configurations(num_configs, containers_template):
    """
    Generates unique random gravity rack configurations.
    """
    configurations = {}
    while len(configurations) < num_configs:
        config = randomize_containers(containers_template)
        # Create a unique key for the configuration
        key = "-".join(
            f"{container['gr_position']}.{content['type']}"
            for container in config.values()
            for content in container["contents"]
        )
        if key not in configurations:
            configurations[key] = config
    return configurations


def generate_kh_configuration(kh_setup, kit_holders_template):
    """
    Generates a kit holder configuration based on the given setup.
    """
    configured_kh = {}
    for idx, kh_id in enumerate(kh_setup, start=1):
        if kh_id in kit_holders_template:
            kh_data = copy.deepcopy(kit_holders_template[kh_id])
            for i, content in enumerate(kh_data["contents"], start=1):
                content["position"] = f"{idx}.{i}"
            configured_kh[f"KH{idx}"] = {
                "kh_position": str(idx),
                "contents": kh_data["contents"]
            }
        else:
            raise ValueError(f"Kit holder ID {kh_id} not found.")
    return configured_kh


def calculate_objective_value(distance_matrix, configuration):
    """
    Calculate the objective value of a given configuration using the exact method.
    """
    # Filter the distance matrix for the given configuration
    filtered_matrix = filter_distance_matrix(distance_matrix, configuration)

    # Solve using the exact method
    tour, cost, _ = run_exact_tsp({
        "data": {
            "distanceMatrix": filtered_matrix,
            "start_node": "0.0",
            "end_node": "0.0.0"
        }
    })
    return cost

# Function to convert data types to native Python types (e.g., for JSON serialization)
def convert_to_native_types(data):
    if isinstance(data, dict):
        return {k: convert_to_native_types(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_to_native_types(v) for v in data]
    elif isinstance(data, pd.DataFrame):
        return data.applymap(lambda x: int(x) if isinstance(x, (np.integer, np.int32, np.int64)) else x).to_dict()
    elif isinstance(data, (np.integer, np.int32, np.int64)):
        return int(data)
    else:
        return data


def run_simulation():
    # Load inputs
    with open("final_distance_matrix.json", "r") as f:
        distance_matrix = json.load(f)

    with open("containers_template.json", "r") as f:
        containers_template = json.load(f)

    with open("kit_holders_template.json", "r") as f:
        kit_holders_template = json.load(f)

    # User-defined inputs
    kh_setup = ["KH001", "KH002", "KH001", "KH003"]
    num_random_gr_configs = 10
    baseline_config = {
    "containers": {
        "Container_1": {
            "gr_position": "1.1",
            "contents": [
                {
                    "position": "1.1.1",
                    "type": "Component_1"
                },
                {
                    "position": "1.1.2",
                    "type": "Component_1"
                },
                {
                    "position": "1.1.3",
                    "type": "Component_1"
                },
                {
                    "position": "1.1.4",
                    "type": "Component_1"
                }
            ]
        },
        "Container_2": {
            "gr_position": "1.2",
            "contents": [
                {
                    "position": "1.2.1",
                    "type": "Component_9"
                },
                {
                    "position": "1.2.2",
                    "type": "Component_9"
                },
                {
                    "position": "1.2.3",
                    "type": "Component_9"
                },
                {
                    "position": "1.2.4",
                    "type": "Component_9"
                }
            ]
        },
        "Container_3": {
            "gr_position": "1.3",
            "contents": [
                {
                    "position": "1.3.1",
                    "type": "Component_11"
                },
                {
                    "position": "1.3.2",
                    "type": "Component_11"
                },
                {
                    "position": "1.3.3",
                    "type": "Component_11"
                },
                {
                    "position": "1.3.4",
                    "type": "Component_11"
                }
            ]
        },
        "Container_4": {
            "gr_position": "1.4",
            "contents": [
                {
                    "position": "1.4.1",
                    "type": "Component_15"
                },
                {
                    "position": "1.4.2",
                    "type": "Component_15"
                },
                {
                    "position": "1.4.3",
                    "type": "Component_15"
                },
                {
                    "position": "1.4.4",
                    "type": "Component_15"
                }
            ]
        },
        "Container_5": {
            "gr_position": "1.5",
            "contents": [
                {
                    "position": "1.5.1",
                    "type": "Component_10"
                },
                {
                    "position": "1.5.2",
                    "type": "Component_10"
                },
                {
                    "position": "1.5.3",
                    "type": "Component_10"
                },
                {
                    "position": "1.5.4",
                    "type": "Component_10"
                }
            ]
        },
        "Container_6": {
            "gr_position": "1.6",
            "contents": [
                {
                    "position": "1.6.1",
                    "type": "Component_16"
                },
                {
                    "position": "1.6.2",
                    "type": "Component_16"
                },
                {
                    "position": "1.6.3",
                    "type": "Component_16"
                },
                {
                    "position": "1.6.4",
                    "type": "Component_16"
                }
            ]
        },
        "Container_7": {
            "gr_position": "1.7",
            "contents": [
                {
                    "position": "1.7.1",
                    "type": "Component_4"
                },
                {
                    "position": "1.7.2",
                    "type": "Component_4"
                },
                {
                    "position": "1.7.3",
                    "type": "Component_4"
                },
                {
                    "position": "1.7.4",
                    "type": "Component_4"
                }
            ]
        },
        "Container_8": {
            "gr_position": "2.1",
            "contents": [
                {
                    "position": "2.1.1",
                    "type": "Component_13"
                },
                {
                    "position": "2.1.2",
                    "type": "Component_13"
                },
                {
                    "position": "2.1.3",
                    "type": "Component_13"
                },
                {
                    "position": "2.1.4",
                    "type": "Component_13"
                }
            ]
        },
        "Container_9": {
            "gr_position": "2.2",
            "contents": [
                {
                    "position": "2.2.1",
                    "type": "Component_3"
                },
                {
                    "position": "2.2.2",
                    "type": "Component_3"
                },
                {
                    "position": "2.2.3",
                    "type": "Component_3"
                },
                {
                    "position": "2.2.4",
                    "type": "Component_3"
                }
            ]
        },
        "Container_10": {
            "gr_position": "2.3",
            "contents": [
                {
                    "position": "2.3.1",
                    "type": "Component_12"
                },
                {
                    "position": "2.3.2",
                    "type": "Component_12"
                },
                {
                    "position": "2.3.3",
                    "type": "Component_12"
                },
                {
                    "position": "2.3.4",
                    "type": "Component_12"
                }
            ]
        },
        "Container_11": {
            "gr_position": "2.4",
            "contents": [
                {
                    "position": "2.4.1",
                    "type": "Component_7"
                },
                {
                    "position": "2.4.2",
                    "type": "Component_7"
                },
                {
                    "position": "2.4.3",
                    "type": "Component_7"
                },
                {
                    "position": "2.4.4",
                    "type": "Component_7"
                }
            ]
        },
        "Container_12": {
            "gr_position": "2.5",
            "contents": [
                {
                    "position": "2.5.1",
                    "type": "Component_14"
                },
                {
                    "position": "2.5.2",
                    "type": "Component_14"
                },
                {
                    "position": "2.5.3",
                    "type": "Component_14"
                },
                {
                    "position": "2.5.4",
                    "type": "Component_14"
                }
            ]
        },
        "Container_13": {
            "gr_position": "2.6",
            "contents": [
                {
                    "position": "2.6.1",
                    "type": "Component_2"
                },
                {
                    "position": "2.6.2",
                    "type": "Component_2"
                },
                {
                    "position": "2.6.3",
                    "type": "Component_2"
                },
                {
                    "position": "2.6.4",
                    "type": "Component_2"
                }
            ]
        },
        "Container_14": {
            "gr_position": "2.7",
            "contents": [
                {
                    "position": "2.7.1",
                    "type": "Component_5"
                },
                {
                    "position": "2.7.2",
                    "type": "Component_5"
                },
                {
                    "position": "2.7.3",
                    "type": "Component_5"
                },
                {
                    "position": "2.7.4",
                    "type": "Component_5"
                }
            ]
        }
    }
    }

    # Generate KH configuration based on setup
    kh_config = generate_kh_configuration(kh_setup, kit_holders_template)

    # Calculate baseline objective value
    baseline_value = calculate_objective_value(distance_matrix, {
        "containers": baseline_config["containers"],
        "kit_holders": kh_config
    })

    # Generate random GR configurations
    gr_configs = generate_unique_gr_configurations(num_random_gr_configs, containers_template)

    # Evaluate random configurations
    best_config = None
    best_value = float("inf")
    results = []
    for key, gr_config in gr_configs.items():
        obj_value = calculate_objective_value(distance_matrix, {
            "containers": gr_config,
            "kit_holders": kh_config
        })
        results.append({"key": key, "objective_value": obj_value})

        if obj_value < best_value:
            best_value = obj_value
            best_config = gr_config

    # Output results
    improvement = ((baseline_value - best_value) / baseline_value) * 100
    output = {
        "baseline_value": baseline_value,
        "best_value": best_value,
        "improvement_percentage": improvement,
        "results": results
    }

    # Convert data to native types before saving
    output_native = convert_to_native_types(output)

    with open("simulation_results.json", "w") as f:
        json.dump(output_native, f, indent=4)
    print("Simulation completed and results saved.")


def compare_gr_configurations(baseline_config, random_configs, distance_matrix):
    results = []
    # Solve for baseline
    baseline_obj_value = solve_exact_method(baseline_config, distance_matrix)
    results.append({"configuration": "Baseline", "objective_value": baseline_obj_value})

    # Solve for random configurations
    for config_key, gr_config in random_configs.items():
        obj_value = solve_exact_method(gr_config, distance_matrix)
        improvement = ((baseline_obj_value - obj_value) / baseline_obj_value) * 100
        results.append({
            "configuration": config_key,
            "objective_value": obj_value,
            "improvement": improvement
        })
    return results

if __name__ == "__main__":
    run_simulation()

