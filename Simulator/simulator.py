import json
import copy
from configurations_final import randomize_containers, filter_distance_matrix
from exact_method import run_exact_tsp
import pandas as pd
import numpy as np
from method_linear import *
from GraphCreation import *

def generate_unique_gr_configurations(num_configs, containers_template):
    """
    unique random gravity rack configurations.
    """
    configurations = {}
    while len(configurations) < num_configs:
        config = randomize_containers(containers_template)
        key = ""

        for container in config.values():
            key += container['gr_position'] + ": " + container["contents"][0]['type'] + " - "

        # unique key for the configuration
        # key = "-".join(
        #     f"{container['gr_position']}.{content['type']}"
            # for container in config.values()
            # for content in container["contents"]
        # )
        if key not in configurations:
            configurations[key] = config
    return configurations


def generate_kh_configuration(kh_setup, kit_holders_template):
    """
    kit holder configuration based on the given setup.
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

from parse_json import create_distance_matrices

def calculate_linear_value(distance_matrix, configuration):
    """
    Calculate the objective value for a given configuration using the linear method.
    """
    # Filter the distance matrix
    filtered_matrix = filter_distance_matrix(distance_matrix, configuration)

    # Create distance matrices and generate the bipartite graph
    a_to_b_matrix = create_distance_matrices({
        "data": {
            "distanceMatrix": filtered_matrix
        }
    })
    # Generate the bipartite graph
    B, set_1, set_2 = create_directed_bipartite_graph(a_to_b_matrix)

    # Define start and end nodes
    start_node = "0.0"
    end_node = "0.0.0"

    # Solve using the linear picking method
    linear_tour = linear_picking(B, start_node, end_node, set_1, set_2)
    tour_cost, _ = total_cost(B, linear_tour["tour"])
    return tour_cost



def calculate_objective_value(distance_matrix, configuration):
    """
    objective value of a given configuration using the exact method.
    """
    # distance matrix for the given configuration
    filtered_matrix = filter_distance_matrix(distance_matrix, configuration)

    # solve using the exact method
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
    # inputs
    with open("final_distance_matrix.json", "r") as f:
        distance_matrix = json.load(f)

    with open("containers_template.json", "r") as f:
        containers_template = json.load(f)

    with open("kit_holders_template.json", "r") as f:
        kit_holders_template = json.load(f)

    # manually inputs
    kh_setup = ["KH001", "KH002", "KH001", "KH003"]
    num_random_gr_configs = 2
    current_config = {
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

    # KH configuration based on kh_setup
    kh_config = generate_kh_configuration(kh_setup, kit_holders_template)

    # Calculate current objective value using Exact Method
    current_exact_value = calculate_objective_value(distance_matrix, {
        "containers": current_config["containers"],
        "kit_holders": kh_config
    })

    # Calculate linear objective value for the current configuration
    current_linear_value = calculate_linear_value(distance_matrix, {
        "containers": current_config["containers"],
        "kit_holders": kh_config
    })

    # random GR configurations
    gr_configs = generate_unique_gr_configurations(num_random_gr_configs, containers_template)

    # evaluate random configurations
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


    output = {
        "current_value_exact": current_exact_value,
        "current_value_linear": current_linear_value,
        "best_value": best_value,
        "improvement_from_exact": round(((current_exact_value - best_value) / current_exact_value) * 100, 4),
        "improvement_from_linear": round(((current_linear_value - best_value) / current_linear_value) * 100, 4),
        "best_configuration": {
            "key": min(results, key=lambda x: x["objective_value"])["key"],
            "objective_value": best_value
        },
        "results": results
    }

    # convert data to native types before saving
    output_native = convert_to_native_types(output)

    with open("simulation_results.json", "w") as f:
        json.dump(output_native, f, indent=4)
    print("Simulation completed and results saved.")


if __name__ == "__main__":
    run_simulation()

