import random
import copy
from itertools import product
import json

# kit holders and containers
kit_holders_template = {
    "KH001": {"contents": [{"position": "", "type": "Component_5"},
                           {"position": "", "type": "Component_15"},
                           {"position": "", "type": "Component_3"},
                           {"position": "", "type": "Component_16"},
                           {"position": "", "type": "Component_14"},
                           {"position": "", "type": "Component_11"}]},
    "KH002": {"contents": [{"position": "", "type": "Component_4"},
                           {"position": "", "type": "Component_2"},
                           {"position": "", "type": "Component_12"},
                           {"position": "", "type": "Component_10"}]},
    "KH003": {"contents": [{"position": "", "type": "Component_9"},
                           {"position": "", "type": "Component_13"},
                           {"position": "", "type": "Component_1"},
                           {"position": "", "type": "Component_7"},
                           {"position": "", "type": "Component_10"}]}
}

containers_template = {
    "Container_1": {"gr_position": "1.1","contents" : [{"position":"1.1.1","type":"Component_1"},
                                                       {"position":"1.1.2","type":"Component_1"},
                                                       {"position":"1.1.3","type":"Component_1"},
                                                       {"position":"1.1.4","type":"Component_1"}]},
    "Container_2": {"gr_position": "1.2","contents" : [{"position":"1.2.1","type":"Component_2"},
                                                       {"position":"1.2.2","type":"Component_2"},
                                                       {"position":"1.2.3","type":"Component_2"},
                                                       {"position":"1.2.4","type":"Component_2"}]},
    "Container_3": {"gr_position": "1.3", "contents": [{"position": "1.3.1", "type": "Component_3"},
                                                       {"position": "1.3.2", "type": "Component_3"},
                                                       {"position": "1.3.3", "type": "Component_3"},
                                                       {"position": "1.3.4", "type": "Component_3"}]},
    "Container_4": {"gr_position": "1.4", "contents": [{"position": "1.4.1", "type": "Component_4"},
                                                       {"position": "1.4.2", "type": "Component_4"},
                                                       {"position": "1.4.3", "type": "Component_4"},
                                                       {"position": "1.4.4", "type": "Component_4"}]},
    "Container_5": {"gr_position": "1.5", "contents": [{"position": "1.5.1", "type": "Component_5"},
                                                       {"position": "1.5.2", "type": "Component_5"},
                                                       {"position": "1.5.3", "type": "Component_5"},
                                                       {"position": "1.5.4", "type": "Component_5"}]},
    "Container_6": {"gr_position": "1.6", "contents": [{"position": "1.6.1", "type": "Component_7"},
                                                       {"position": "1.6.2", "type": "Component_7"},
                                                       {"position": "1.6.3", "type": "Component_7"},
                                                       {"position": "1.6.4", "type": "Component_7"}]},
    "Container_7": {"gr_position": "1.7", "contents": [{"position": "1.7.1", "type": "Component_9"},
                                                       {"position": "1.7.2", "type": "Component_9"},
                                                       {"position": "1.7.3", "type": "Component_9"},
                                                       {"position": "1.7.4", "type": "Component_9"}]},
    "Container_8": {"gr_position": "1.8", "contents": [{"position": "2.1.1", "type": "Component_10"},
                                                       {"position": "2.1.2", "type": "Component_10"},
                                                       {"position": "2.1.3", "type": "Component_10"},
                                                       {"position": "2.1.4", "type": "Component_10"}]},
    "Container_9": {"gr_position": "1.9", "contents": [{"position": "2.2.1", "type": "Component_11"},
                                                       {"position": "2.2.2", "type": "Component_11"},
                                                       {"position": "2.2.3", "type": "Component_11"},
                                                       {"position": "2.2.4", "type": "Component_11"}]},
    "Container_10": {"gr_position": "1.10", "contents": [{"position": "2.3.1", "type": "Component_12"},
                                                       {"position": "2.3.2", "type": "Component_12"},
                                                       {"position": "2.3.3", "type": "Component_12"},
                                                       {"position": "2.3.4", "type": "Component_12"}]},
    "Container_11": {"gr_position": "1.11", "contents": [{"position": "2.4.1", "type": "Component_13"},
                                                       {"position": "2.4.2", "type": "Component_13"},
                                                       {"position": "2.4.3", "type": "Component_13"},
                                                       {"position": "2.4.4", "type": "Component_13"}]},
    "Container_12": {"gr_position": "1.12", "contents": [{"position": "2.5.1", "type": "Component_14"},
                                                       {"position": "2.5.2", "type": "Component_14"},
                                                       {"position": "2.5.3", "type": "Component_14"},
                                                       {"position": "2.5.4", "type": "Component_14"}]},
    "Container_13": {"gr_position": "1.13", "contents": [{"position": "2.6.1", "type": "Component_15"},
                                                       {"position": "2.6.2", "type": "Component_15"},
                                                       {"position": "2.6.3", "type": "Component_15"},
                                                       {"position": "2.6.4", "type": "Component_15"}]},
    "Container_14": {"gr_position": "1.14", "contents": [{"position": "2.7.1", "type": "Component_16"},
                                                       {"position": "2.7.2", "type": "Component_16"},
                                                       {"position": "2.7.3", "type": "Component_16"},
                                                       {"position": "2.7.4", "type": "Component_16"}]}
}

def generate_all_kh_configurations(kit_holders, num_positions=4):
    kh_keys = list(kit_holders.keys())
    all_combinations = list(product(kh_keys, repeat=num_positions))  # cartesian product
    random.shuffle(all_combinations)  # randomness for configurations
    return all_combinations

def randomize_kit_holders(kit_holders, configuration):
    """
    Assign kit holders to positions based on a specific configuration.
    """
    new_kit_holders = {}
    for pos_idx, kh_key in enumerate(configuration, start=1):
        kh_data = copy.deepcopy(kit_holders[kh_key])
        new_contents = []

        # Update positions dynamically
        for i, content in enumerate(kh_data["contents"], start=1):
            content["position"] = f"{pos_idx}.{i}"
            new_contents.append(content)

        new_kit_holders[f"KH{pos_idx}"] = {
            "kh_position": str(pos_idx),
            "contents": new_contents,
        }

    return new_kit_holders

def randomize_containers(containers_template):
    """
    Randomly assign components to containers, ensuring correct numbering:
    - First group: 1.1 to 1.7
    - Second group: 2.1 to 2.7
    Each container has 4 positions with the same component type.
    """
    # extract all unique component types
    all_components = []
    for container in containers_template.values():
        for content in container["contents"]:
            if content["type"] not in all_components:
                all_components.append(content["type"])

    # randomness for the component types
    random.shuffle(all_components)

    # Create new containers with updated numbering
    new_containers = {}
    for idx, container_key in enumerate(containers_template.keys(), start=1):
        group = 1 if idx <= 7 else 2  # 1.x or 2.x range
        subgroup = idx if group == 1 else idx - 7
        gr_position = f"{group}.{subgroup}"  # e.g., 1.1, 2.1

        component_type = all_components[(idx - 1) % len(all_components)]  # cycle components
        new_contents = [
            {"position": f"{gr_position}.{i}", "type": component_type}  # hierarchical positions
            for i in range(1, 5)
        ]

        new_containers[container_key] = {"gr_position": gr_position, "contents": new_contents}

    return new_containers

def generate_random_configuration(containers, kit_holders):
    """
    Generate a random configuration of containers and kit holders.
    """
    all_kh_configs = generate_all_kh_configurations(kit_holders, num_positions=4)
    selected_config = random.choice(all_kh_configs)
    randomized_kit_holders = randomize_kit_holders(kit_holders, selected_config)
    randomized_containers = randomize_containers(containers)
    return {"containers": randomized_containers, "kit_holders": randomized_kit_holders}

containers = copy.deepcopy(containers_template)
kit_holders = copy.deepcopy(kit_holders_template)

# Generate one random configuration
random_config = generate_random_configuration(containers, kit_holders)
print("Randomized Configuration:")
print(random_config)

distance_matrix = {
    "0.0": [
        {
            "1.1": [
                {
                    "node": "1.1.1",
                    "distance": 16776
                },
                {
                    "node": "1.1.2",
                    "distance": 16776
                },
                {
                    "node": "1.1.3",
                    "distance": 16776
                },
                {
                    "node": "1.1.4",
                    "distance": 16776
                },
                {
                    "node": "1.2.1",
                    "distance": 16776
                },
                {
                    "node": "1.2.2",
                    "distance": 16776
                },
                {
                    "node": "1.2.3",
                    "distance": 16776
                },
                {
                    "node": "1.2.4",
                    "distance": 16776
                },
                {
                    "node": "1.3.1",
                    "distance": 16776
                },
                {
                    "node": "1.3.2",
                    "distance": 16776
                },
                {
                    "node": "1.3.3",
                    "distance": 16776
                },
                {
                    "node": "1.3.4",
                    "distance": 16776
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 27230
                },
                {
                    "node": "1.5.2",
                    "distance": 27230
                },
                {
                    "node": "1.5.3",
                    "distance": 27230
                },
                {
                    "node": "1.5.4",
                    "distance": 27230
                },
                {
                    "node": "1.6.1",
                    "distance": 33628
                },
                {
                    "node": "1.6.2",
                    "distance": 33628
                },
                {
                    "node": "1.6.3",
                    "distance": 33628
                },
                {
                    "node": "1.6.4",
                    "distance": 33628
                },
                {
                    "node": "1.7.1",
                    "distance": 40110
                },
                {
                    "node": "1.7.2",
                    "distance": 40110
                },
                {
                    "node": "1.7.3",
                    "distance": 40110
                },
                {
                    "node": "1.7.4",
                    "distance": 40110
                },
                {
                    "node": "2.1.1",
                    "distance": 16752
                },
                {
                    "node": "2.1.2",
                    "distance": 16752
                },
                {
                    "node": "2.1.3",
                    "distance": 16752
                },
                {
                    "node": "2.1.4",
                    "distance": 16752
                },
                {
                    "node": "2.2.1",
                    "distance": 16752
                },
                {
                    "node": "2.2.2",
                    "distance": 16752
                },
                {
                    "node": "2.2.3",
                    "distance": 16752
                },
                {
                    "node": "2.2.4",
                    "distance": 16752
                },
                {
                    "node": "2.3.1",
                    "distance": 16752
                },
                {
                    "node": "2.3.2",
                    "distance": 16752
                },
                {
                    "node": "2.3.3",
                    "distance": 16752
                },
                {
                    "node": "2.3.4",
                    "distance": 16752
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 27230
                },
                {
                    "node": "2.5.2",
                    "distance": 27230
                },
                {
                    "node": "2.5.3",
                    "distance": 27230
                },
                {
                    "node": "2.5.4",
                    "distance": 27230
                },
                {
                    "node": "2.6.1",
                    "distance": 33628
                },
                {
                    "node": "2.6.2",
                    "distance": 33628
                },
                {
                    "node": "2.6.3",
                    "distance": 33628
                },
                {
                    "node": "2.6.4",
                    "distance": 33628
                },
                {
                    "node": "2.7.1",
                    "distance": 40110
                },
                {
                    "node": "2.7.2",
                    "distance": 40110
                },
                {
                    "node": "2.7.3",
                    "distance": 40110
                },
                {
                    "node": "2.7.4",
                    "distance": 40110
                }
            ]
        },
        {
            "1.2": [
                {
                    "node": "1.1.1",
                    "distance": 16776
                },
                {
                    "node": "1.1.2",
                    "distance": 16776
                },
                {
                    "node": "1.1.3",
                    "distance": 16776
                },
                {
                    "node": "1.1.4",
                    "distance": 16776
                },
                {
                    "node": "1.2.1",
                    "distance": 16776
                },
                {
                    "node": "1.2.2",
                    "distance": 16776
                },
                {
                    "node": "1.2.3",
                    "distance": 16776
                },
                {
                    "node": "1.2.4",
                    "distance": 16776
                },
                {
                    "node": "1.3.1",
                    "distance": 16776
                },
                {
                    "node": "1.3.2",
                    "distance": 16776
                },
                {
                    "node": "1.3.3",
                    "distance": 16776
                },
                {
                    "node": "1.3.4",
                    "distance": 16776
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 27230
                },
                {
                    "node": "1.5.2",
                    "distance": 27230
                },
                {
                    "node": "1.5.3",
                    "distance": 27230
                },
                {
                    "node": "1.5.4",
                    "distance": 27230
                },
                {
                    "node": "1.6.1",
                    "distance": 33628
                },
                {
                    "node": "1.6.2",
                    "distance": 33628
                },
                {
                    "node": "1.6.3",
                    "distance": 33628
                },
                {
                    "node": "1.6.4",
                    "distance": 33628
                },
                {
                    "node": "1.7.1",
                    "distance": 40110
                },
                {
                    "node": "1.7.2",
                    "distance": 40110
                },
                {
                    "node": "1.7.3",
                    "distance": 40110
                },
                {
                    "node": "1.7.4",
                    "distance": 40110
                },
                {
                    "node": "2.1.1",
                    "distance": 16752
                },
                {
                    "node": "2.1.2",
                    "distance": 16752
                },
                {
                    "node": "2.1.3",
                    "distance": 16752
                },
                {
                    "node": "2.1.4",
                    "distance": 16752
                },
                {
                    "node": "2.2.1",
                    "distance": 16752
                },
                {
                    "node": "2.2.2",
                    "distance": 16752
                },
                {
                    "node": "2.2.3",
                    "distance": 16752
                },
                {
                    "node": "2.2.4",
                    "distance": 16752
                },
                {
                    "node": "2.3.1",
                    "distance": 16752
                },
                {
                    "node": "2.3.2",
                    "distance": 16752
                },
                {
                    "node": "2.3.3",
                    "distance": 16752
                },
                {
                    "node": "2.3.4",
                    "distance": 16752
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 27230
                },
                {
                    "node": "2.5.2",
                    "distance": 27230
                },
                {
                    "node": "2.5.3",
                    "distance": 27230
                },
                {
                    "node": "2.5.4",
                    "distance": 27230
                },
                {
                    "node": "2.6.1",
                    "distance": 33628
                },
                {
                    "node": "2.6.2",
                    "distance": 33628
                },
                {
                    "node": "2.6.3",
                    "distance": 33628
                },
                {
                    "node": "2.6.4",
                    "distance": 33628
                },
                {
                    "node": "2.7.1",
                    "distance": 40110
                },
                {
                    "node": "2.7.2",
                    "distance": 40110
                },
                {
                    "node": "2.7.3",
                    "distance": 40110
                },
                {
                    "node": "2.7.4",
                    "distance": 40110
                }
            ]
        },
        {
            "1.3": [
                {
                    "node": "1.1.1",
                    "distance": 16776
                },
                {
                    "node": "1.1.2",
                    "distance": 16776
                },
                {
                    "node": "1.1.3",
                    "distance": 16776
                },
                {
                    "node": "1.1.4",
                    "distance": 16776
                },
                {
                    "node": "1.2.1",
                    "distance": 16776
                },
                {
                    "node": "1.2.2",
                    "distance": 16776
                },
                {
                    "node": "1.2.3",
                    "distance": 16776
                },
                {
                    "node": "1.2.4",
                    "distance": 16776
                },
                {
                    "node": "1.3.1",
                    "distance": 16776
                },
                {
                    "node": "1.3.2",
                    "distance": 16776
                },
                {
                    "node": "1.3.3",
                    "distance": 16776
                },
                {
                    "node": "1.3.4",
                    "distance": 16776
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 27230
                },
                {
                    "node": "1.5.2",
                    "distance": 27230
                },
                {
                    "node": "1.5.3",
                    "distance": 27230
                },
                {
                    "node": "1.5.4",
                    "distance": 27230
                },
                {
                    "node": "1.6.1",
                    "distance": 33628
                },
                {
                    "node": "1.6.2",
                    "distance": 33628
                },
                {
                    "node": "1.6.3",
                    "distance": 33628
                },
                {
                    "node": "1.6.4",
                    "distance": 33628
                },
                {
                    "node": "1.7.1",
                    "distance": 40110
                },
                {
                    "node": "1.7.2",
                    "distance": 40110
                },
                {
                    "node": "1.7.3",
                    "distance": 40110
                },
                {
                    "node": "1.7.4",
                    "distance": 40110
                },
                {
                    "node": "2.1.1",
                    "distance": 16752
                },
                {
                    "node": "2.1.2",
                    "distance": 16752
                },
                {
                    "node": "2.1.3",
                    "distance": 16752
                },
                {
                    "node": "2.1.4",
                    "distance": 16752
                },
                {
                    "node": "2.2.1",
                    "distance": 16752
                },
                {
                    "node": "2.2.2",
                    "distance": 16752
                },
                {
                    "node": "2.2.3",
                    "distance": 16752
                },
                {
                    "node": "2.2.4",
                    "distance": 16752
                },
                {
                    "node": "2.3.1",
                    "distance": 16752
                },
                {
                    "node": "2.3.2",
                    "distance": 16752
                },
                {
                    "node": "2.3.3",
                    "distance": 16752
                },
                {
                    "node": "2.3.4",
                    "distance": 16752
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 27230
                },
                {
                    "node": "2.5.2",
                    "distance": 27230
                },
                {
                    "node": "2.5.3",
                    "distance": 27230
                },
                {
                    "node": "2.5.4",
                    "distance": 27230
                },
                {
                    "node": "2.6.1",
                    "distance": 33628
                },
                {
                    "node": "2.6.2",
                    "distance": 33628
                },
                {
                    "node": "2.6.3",
                    "distance": 33628
                },
                {
                    "node": "2.6.4",
                    "distance": 33628
                },
                {
                    "node": "2.7.1",
                    "distance": 40110
                },
                {
                    "node": "2.7.2",
                    "distance": 40110
                },
                {
                    "node": "2.7.3",
                    "distance": 40110
                },
                {
                    "node": "2.7.4",
                    "distance": 40110
                }
            ]
        },
        {
            "1.4": [
                {
                    "node": "1.1.1",
                    "distance": 16776
                },
                {
                    "node": "1.1.2",
                    "distance": 16776
                },
                {
                    "node": "1.1.3",
                    "distance": 16776
                },
                {
                    "node": "1.1.4",
                    "distance": 16776
                },
                {
                    "node": "1.2.1",
                    "distance": 16776
                },
                {
                    "node": "1.2.2",
                    "distance": 16776
                },
                {
                    "node": "1.2.3",
                    "distance": 16776
                },
                {
                    "node": "1.2.4",
                    "distance": 16776
                },
                {
                    "node": "1.3.1",
                    "distance": 16776
                },
                {
                    "node": "1.3.2",
                    "distance": 16776
                },
                {
                    "node": "1.3.3",
                    "distance": 16776
                },
                {
                    "node": "1.3.4",
                    "distance": 16776
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 27230
                },
                {
                    "node": "1.5.2",
                    "distance": 27230
                },
                {
                    "node": "1.5.3",
                    "distance": 27230
                },
                {
                    "node": "1.5.4",
                    "distance": 27230
                },
                {
                    "node": "1.6.1",
                    "distance": 33628
                },
                {
                    "node": "1.6.2",
                    "distance": 33628
                },
                {
                    "node": "1.6.3",
                    "distance": 33628
                },
                {
                    "node": "1.6.4",
                    "distance": 33628
                },
                {
                    "node": "1.7.1",
                    "distance": 40110
                },
                {
                    "node": "1.7.2",
                    "distance": 40110
                },
                {
                    "node": "1.7.3",
                    "distance": 40110
                },
                {
                    "node": "1.7.4",
                    "distance": 40110
                },
                {
                    "node": "2.1.1",
                    "distance": 16752
                },
                {
                    "node": "2.1.2",
                    "distance": 16752
                },
                {
                    "node": "2.1.3",
                    "distance": 16752
                },
                {
                    "node": "2.1.4",
                    "distance": 16752
                },
                {
                    "node": "2.2.1",
                    "distance": 16752
                },
                {
                    "node": "2.2.2",
                    "distance": 16752
                },
                {
                    "node": "2.2.3",
                    "distance": 16752
                },
                {
                    "node": "2.2.4",
                    "distance": 16752
                },
                {
                    "node": "2.3.1",
                    "distance": 16752
                },
                {
                    "node": "2.3.2",
                    "distance": 16752
                },
                {
                    "node": "2.3.3",
                    "distance": 16752
                },
                {
                    "node": "2.3.4",
                    "distance": 16752
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 27230
                },
                {
                    "node": "2.5.2",
                    "distance": 27230
                },
                {
                    "node": "2.5.3",
                    "distance": 27230
                },
                {
                    "node": "2.5.4",
                    "distance": 27230
                },
                {
                    "node": "2.6.1",
                    "distance": 33628
                },
                {
                    "node": "2.6.2",
                    "distance": 33628
                },
                {
                    "node": "2.6.3",
                    "distance": 33628
                },
                {
                    "node": "2.6.4",
                    "distance": 33628
                },
                {
                    "node": "2.7.1",
                    "distance": 40110
                },
                {
                    "node": "2.7.2",
                    "distance": 40110
                },
                {
                    "node": "2.7.3",
                    "distance": 40110
                },
                {
                    "node": "2.7.4",
                    "distance": 40110
                }
            ]
        },
        {
            "1.5": [
                {
                    "node": "1.1.1",
                    "distance": 16776
                },
                {
                    "node": "1.1.2",
                    "distance": 16776
                },
                {
                    "node": "1.1.3",
                    "distance": 16776
                },
                {
                    "node": "1.1.4",
                    "distance": 16776
                },
                {
                    "node": "1.2.1",
                    "distance": 16776
                },
                {
                    "node": "1.2.2",
                    "distance": 16776
                },
                {
                    "node": "1.2.3",
                    "distance": 16776
                },
                {
                    "node": "1.2.4",
                    "distance": 16776
                },
                {
                    "node": "1.3.1",
                    "distance": 16776
                },
                {
                    "node": "1.3.2",
                    "distance": 16776
                },
                {
                    "node": "1.3.3",
                    "distance": 16776
                },
                {
                    "node": "1.3.4",
                    "distance": 16776
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 27230
                },
                {
                    "node": "1.5.2",
                    "distance": 27230
                },
                {
                    "node": "1.5.3",
                    "distance": 27230
                },
                {
                    "node": "1.5.4",
                    "distance": 27230
                },
                {
                    "node": "1.6.1",
                    "distance": 33628
                },
                {
                    "node": "1.6.2",
                    "distance": 33628
                },
                {
                    "node": "1.6.3",
                    "distance": 33628
                },
                {
                    "node": "1.6.4",
                    "distance": 33628
                },
                {
                    "node": "1.7.1",
                    "distance": 40110
                },
                {
                    "node": "1.7.2",
                    "distance": 40110
                },
                {
                    "node": "1.7.3",
                    "distance": 40110
                },
                {
                    "node": "1.7.4",
                    "distance": 40110
                },
                {
                    "node": "2.1.1",
                    "distance": 16752
                },
                {
                    "node": "2.1.2",
                    "distance": 16752
                },
                {
                    "node": "2.1.3",
                    "distance": 16752
                },
                {
                    "node": "2.1.4",
                    "distance": 16752
                },
                {
                    "node": "2.2.1",
                    "distance": 16752
                },
                {
                    "node": "2.2.2",
                    "distance": 16752
                },
                {
                    "node": "2.2.3",
                    "distance": 16752
                },
                {
                    "node": "2.2.4",
                    "distance": 16752
                },
                {
                    "node": "2.3.1",
                    "distance": 16752
                },
                {
                    "node": "2.3.2",
                    "distance": 16752
                },
                {
                    "node": "2.3.3",
                    "distance": 16752
                },
                {
                    "node": "2.3.4",
                    "distance": 16752
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 27230
                },
                {
                    "node": "2.5.2",
                    "distance": 27230
                },
                {
                    "node": "2.5.3",
                    "distance": 27230
                },
                {
                    "node": "2.5.4",
                    "distance": 27230
                },
                {
                    "node": "2.6.1",
                    "distance": 33628
                },
                {
                    "node": "2.6.2",
                    "distance": 33628
                },
                {
                    "node": "2.6.3",
                    "distance": 33628
                },
                {
                    "node": "2.6.4",
                    "distance": 33628
                },
                {
                    "node": "2.7.1",
                    "distance": 40110
                },
                {
                    "node": "2.7.2",
                    "distance": 40110
                },
                {
                    "node": "2.7.3",
                    "distance": 40110
                },
                {
                    "node": "2.7.4",
                    "distance": 40110
                }
            ]
        },
        {
            "1.6": [
                {
                    "node": "1.1.1",
                    "distance": 16776
                },
                {
                    "node": "1.1.2",
                    "distance": 16776
                },
                {
                    "node": "1.1.3",
                    "distance": 16776
                },
                {
                    "node": "1.1.4",
                    "distance": 16776
                },
                {
                    "node": "1.2.1",
                    "distance": 16776
                },
                {
                    "node": "1.2.2",
                    "distance": 16776
                },
                {
                    "node": "1.2.3",
                    "distance": 16776
                },
                {
                    "node": "1.2.4",
                    "distance": 16776
                },
                {
                    "node": "1.3.1",
                    "distance": 16776
                },
                {
                    "node": "1.3.2",
                    "distance": 16776
                },
                {
                    "node": "1.3.3",
                    "distance": 16776
                },
                {
                    "node": "1.3.4",
                    "distance": 16776
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 27230
                },
                {
                    "node": "1.5.2",
                    "distance": 27230
                },
                {
                    "node": "1.5.3",
                    "distance": 27230
                },
                {
                    "node": "1.5.4",
                    "distance": 27230
                },
                {
                    "node": "1.6.1",
                    "distance": 33628
                },
                {
                    "node": "1.6.2",
                    "distance": 33628
                },
                {
                    "node": "1.6.3",
                    "distance": 33628
                },
                {
                    "node": "1.6.4",
                    "distance": 33628
                },
                {
                    "node": "1.7.1",
                    "distance": 40110
                },
                {
                    "node": "1.7.2",
                    "distance": 40110
                },
                {
                    "node": "1.7.3",
                    "distance": 40110
                },
                {
                    "node": "1.7.4",
                    "distance": 40110
                },
                {
                    "node": "2.1.1",
                    "distance": 16752
                },
                {
                    "node": "2.1.2",
                    "distance": 16752
                },
                {
                    "node": "2.1.3",
                    "distance": 16752
                },
                {
                    "node": "2.1.4",
                    "distance": 16752
                },
                {
                    "node": "2.2.1",
                    "distance": 16752
                },
                {
                    "node": "2.2.2",
                    "distance": 16752
                },
                {
                    "node": "2.2.3",
                    "distance": 16752
                },
                {
                    "node": "2.2.4",
                    "distance": 16752
                },
                {
                    "node": "2.3.1",
                    "distance": 16752
                },
                {
                    "node": "2.3.2",
                    "distance": 16752
                },
                {
                    "node": "2.3.3",
                    "distance": 16752
                },
                {
                    "node": "2.3.4",
                    "distance": 16752
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 27230
                },
                {
                    "node": "2.5.2",
                    "distance": 27230
                },
                {
                    "node": "2.5.3",
                    "distance": 27230
                },
                {
                    "node": "2.5.4",
                    "distance": 27230
                },
                {
                    "node": "2.6.1",
                    "distance": 33628
                },
                {
                    "node": "2.6.2",
                    "distance": 33628
                },
                {
                    "node": "2.6.3",
                    "distance": 33628
                },
                {
                    "node": "2.6.4",
                    "distance": 33628
                },
                {
                    "node": "2.7.1",
                    "distance": 40110
                },
                {
                    "node": "2.7.2",
                    "distance": 40110
                },
                {
                    "node": "2.7.3",
                    "distance": 40110
                },
                {
                    "node": "2.7.4",
                    "distance": 40110
                }
            ]
        },
        {
            "2.1": [
                {
                    "node": "1.1.1",
                    "distance": 16776
                },
                {
                    "node": "1.1.2",
                    "distance": 16776
                },
                {
                    "node": "1.1.3",
                    "distance": 16776
                },
                {
                    "node": "1.1.4",
                    "distance": 16776
                },
                {
                    "node": "1.2.1",
                    "distance": 16776
                },
                {
                    "node": "1.2.2",
                    "distance": 16776
                },
                {
                    "node": "1.2.3",
                    "distance": 16776
                },
                {
                    "node": "1.2.4",
                    "distance": 16776
                },
                {
                    "node": "1.3.1",
                    "distance": 16776
                },
                {
                    "node": "1.3.2",
                    "distance": 16776
                },
                {
                    "node": "1.3.3",
                    "distance": 16776
                },
                {
                    "node": "1.3.4",
                    "distance": 16776
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 27257
                },
                {
                    "node": "1.6.2",
                    "distance": 27257
                },
                {
                    "node": "1.6.3",
                    "distance": 27257
                },
                {
                    "node": "1.6.4",
                    "distance": 27257
                },
                {
                    "node": "1.7.1",
                    "distance": 33670
                },
                {
                    "node": "1.7.2",
                    "distance": 33670
                },
                {
                    "node": "1.7.3",
                    "distance": 33670
                },
                {
                    "node": "1.7.4",
                    "distance": 33670
                },
                {
                    "node": "2.1.1",
                    "distance": 16752
                },
                {
                    "node": "2.1.2",
                    "distance": 16752
                },
                {
                    "node": "2.1.3",
                    "distance": 16752
                },
                {
                    "node": "2.1.4",
                    "distance": 16752
                },
                {
                    "node": "2.2.1",
                    "distance": 16752
                },
                {
                    "node": "2.2.2",
                    "distance": 16752
                },
                {
                    "node": "2.2.3",
                    "distance": 16752
                },
                {
                    "node": "2.2.4",
                    "distance": 16752
                },
                {
                    "node": "2.3.1",
                    "distance": 16752
                },
                {
                    "node": "2.3.2",
                    "distance": 16752
                },
                {
                    "node": "2.3.3",
                    "distance": 16752
                },
                {
                    "node": "2.3.4",
                    "distance": 16752
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 27257
                },
                {
                    "node": "2.6.2",
                    "distance": 27257
                },
                {
                    "node": "2.6.3",
                    "distance": 27257
                },
                {
                    "node": "2.6.4",
                    "distance": 27257
                },
                {
                    "node": "2.7.1",
                    "distance": 33670
                },
                {
                    "node": "2.7.2",
                    "distance": 33670
                },
                {
                    "node": "2.7.3",
                    "distance": 33670
                },
                {
                    "node": "2.7.4",
                    "distance": 33670
                }
            ]
        },
        {
            "2.2": [
                {
                    "node": "1.1.1",
                    "distance": 16776
                },
                {
                    "node": "1.1.2",
                    "distance": 16776
                },
                {
                    "node": "1.1.3",
                    "distance": 16776
                },
                {
                    "node": "1.1.4",
                    "distance": 16776
                },
                {
                    "node": "1.2.1",
                    "distance": 16776
                },
                {
                    "node": "1.2.2",
                    "distance": 16776
                },
                {
                    "node": "1.2.3",
                    "distance": 16776
                },
                {
                    "node": "1.2.4",
                    "distance": 16776
                },
                {
                    "node": "1.3.1",
                    "distance": 16776
                },
                {
                    "node": "1.3.2",
                    "distance": 16776
                },
                {
                    "node": "1.3.3",
                    "distance": 16776
                },
                {
                    "node": "1.3.4",
                    "distance": 16776
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 27257
                },
                {
                    "node": "1.6.2",
                    "distance": 27257
                },
                {
                    "node": "1.6.3",
                    "distance": 27257
                },
                {
                    "node": "1.6.4",
                    "distance": 27257
                },
                {
                    "node": "1.7.1",
                    "distance": 33670
                },
                {
                    "node": "1.7.2",
                    "distance": 33670
                },
                {
                    "node": "1.7.3",
                    "distance": 33670
                },
                {
                    "node": "1.7.4",
                    "distance": 33670
                },
                {
                    "node": "2.1.1",
                    "distance": 16752
                },
                {
                    "node": "2.1.2",
                    "distance": 16752
                },
                {
                    "node": "2.1.3",
                    "distance": 16752
                },
                {
                    "node": "2.1.4",
                    "distance": 16752
                },
                {
                    "node": "2.2.1",
                    "distance": 16752
                },
                {
                    "node": "2.2.2",
                    "distance": 16752
                },
                {
                    "node": "2.2.3",
                    "distance": 16752
                },
                {
                    "node": "2.2.4",
                    "distance": 16752
                },
                {
                    "node": "2.3.1",
                    "distance": 16752
                },
                {
                    "node": "2.3.2",
                    "distance": 16752
                },
                {
                    "node": "2.3.3",
                    "distance": 16752
                },
                {
                    "node": "2.3.4",
                    "distance": 16752
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 27257
                },
                {
                    "node": "2.6.2",
                    "distance": 27257
                },
                {
                    "node": "2.6.3",
                    "distance": 27257
                },
                {
                    "node": "2.6.4",
                    "distance": 27257
                },
                {
                    "node": "2.7.1",
                    "distance": 33670
                },
                {
                    "node": "2.7.2",
                    "distance": 33670
                },
                {
                    "node": "2.7.3",
                    "distance": 33670
                },
                {
                    "node": "2.7.4",
                    "distance": 33670
                }
            ]
        },
        {
            "2.3": [
                {
                    "node": "1.1.1",
                    "distance": 16776
                },
                {
                    "node": "1.1.2",
                    "distance": 16776
                },
                {
                    "node": "1.1.3",
                    "distance": 16776
                },
                {
                    "node": "1.1.4",
                    "distance": 16776
                },
                {
                    "node": "1.2.1",
                    "distance": 16776
                },
                {
                    "node": "1.2.2",
                    "distance": 16776
                },
                {
                    "node": "1.2.3",
                    "distance": 16776
                },
                {
                    "node": "1.2.4",
                    "distance": 16776
                },
                {
                    "node": "1.3.1",
                    "distance": 16776
                },
                {
                    "node": "1.3.2",
                    "distance": 16776
                },
                {
                    "node": "1.3.3",
                    "distance": 16776
                },
                {
                    "node": "1.3.4",
                    "distance": 16776
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 27257
                },
                {
                    "node": "1.6.2",
                    "distance": 27257
                },
                {
                    "node": "1.6.3",
                    "distance": 27257
                },
                {
                    "node": "1.6.4",
                    "distance": 27257
                },
                {
                    "node": "1.7.1",
                    "distance": 33670
                },
                {
                    "node": "1.7.2",
                    "distance": 33670
                },
                {
                    "node": "1.7.3",
                    "distance": 33670
                },
                {
                    "node": "1.7.4",
                    "distance": 33670
                },
                {
                    "node": "2.1.1",
                    "distance": 16752
                },
                {
                    "node": "2.1.2",
                    "distance": 16752
                },
                {
                    "node": "2.1.3",
                    "distance": 16752
                },
                {
                    "node": "2.1.4",
                    "distance": 16752
                },
                {
                    "node": "2.2.1",
                    "distance": 16752
                },
                {
                    "node": "2.2.2",
                    "distance": 16752
                },
                {
                    "node": "2.2.3",
                    "distance": 16752
                },
                {
                    "node": "2.2.4",
                    "distance": 16752
                },
                {
                    "node": "2.3.1",
                    "distance": 16752
                },
                {
                    "node": "2.3.2",
                    "distance": 16752
                },
                {
                    "node": "2.3.3",
                    "distance": 16752
                },
                {
                    "node": "2.3.4",
                    "distance": 16752
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 27257
                },
                {
                    "node": "2.6.2",
                    "distance": 27257
                },
                {
                    "node": "2.6.3",
                    "distance": 27257
                },
                {
                    "node": "2.6.4",
                    "distance": 27257
                },
                {
                    "node": "2.7.1",
                    "distance": 33670
                },
                {
                    "node": "2.7.2",
                    "distance": 33670
                },
                {
                    "node": "2.7.3",
                    "distance": 33670
                },
                {
                    "node": "2.7.4",
                    "distance": 33670
                }
            ]
        },
        {
            "2.4": [
                {
                    "node": "1.1.1",
                    "distance": 16776
                },
                {
                    "node": "1.1.2",
                    "distance": 16776
                },
                {
                    "node": "1.1.3",
                    "distance": 16776
                },
                {
                    "node": "1.1.4",
                    "distance": 16776
                },
                {
                    "node": "1.2.1",
                    "distance": 16776
                },
                {
                    "node": "1.2.2",
                    "distance": 16776
                },
                {
                    "node": "1.2.3",
                    "distance": 16776
                },
                {
                    "node": "1.2.4",
                    "distance": 16776
                },
                {
                    "node": "1.3.1",
                    "distance": 16776
                },
                {
                    "node": "1.3.2",
                    "distance": 16776
                },
                {
                    "node": "1.3.3",
                    "distance": 16776
                },
                {
                    "node": "1.3.4",
                    "distance": 16776
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 27257
                },
                {
                    "node": "1.6.2",
                    "distance": 27257
                },
                {
                    "node": "1.6.3",
                    "distance": 27257
                },
                {
                    "node": "1.6.4",
                    "distance": 27257
                },
                {
                    "node": "1.7.1",
                    "distance": 33670
                },
                {
                    "node": "1.7.2",
                    "distance": 33670
                },
                {
                    "node": "1.7.3",
                    "distance": 33670
                },
                {
                    "node": "1.7.4",
                    "distance": 33670
                },
                {
                    "node": "2.1.1",
                    "distance": 16752
                },
                {
                    "node": "2.1.2",
                    "distance": 16752
                },
                {
                    "node": "2.1.3",
                    "distance": 16752
                },
                {
                    "node": "2.1.4",
                    "distance": 16752
                },
                {
                    "node": "2.2.1",
                    "distance": 16752
                },
                {
                    "node": "2.2.2",
                    "distance": 16752
                },
                {
                    "node": "2.2.3",
                    "distance": 16752
                },
                {
                    "node": "2.2.4",
                    "distance": 16752
                },
                {
                    "node": "2.3.1",
                    "distance": 16752
                },
                {
                    "node": "2.3.2",
                    "distance": 16752
                },
                {
                    "node": "2.3.3",
                    "distance": 16752
                },
                {
                    "node": "2.3.4",
                    "distance": 16752
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 27257
                },
                {
                    "node": "2.6.2",
                    "distance": 27257
                },
                {
                    "node": "2.6.3",
                    "distance": 27257
                },
                {
                    "node": "2.6.4",
                    "distance": 27257
                },
                {
                    "node": "2.7.1",
                    "distance": 33670
                },
                {
                    "node": "2.7.2",
                    "distance": 33670
                },
                {
                    "node": "2.7.3",
                    "distance": 33670
                },
                {
                    "node": "2.7.4",
                    "distance": 33670
                }
            ]
        },
        {
            "2.5": [
                {
                    "node": "1.1.1",
                    "distance": 21130
                },
                {
                    "node": "1.1.2",
                    "distance": 21130
                },
                {
                    "node": "1.1.3",
                    "distance": 21130
                },
                {
                    "node": "1.1.4",
                    "distance": 21130
                },
                {
                    "node": "1.2.1",
                    "distance": 17958
                },
                {
                    "node": "1.2.2",
                    "distance": 17958
                },
                {
                    "node": "1.2.3",
                    "distance": 17958
                },
                {
                    "node": "1.2.4",
                    "distance": 17958
                },
                {
                    "node": "1.3.1",
                    "distance": 16776
                },
                {
                    "node": "1.3.2",
                    "distance": 16776
                },
                {
                    "node": "1.3.3",
                    "distance": 16776
                },
                {
                    "node": "1.3.4",
                    "distance": 16776
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 21394
                },
                {
                    "node": "2.1.2",
                    "distance": 21394
                },
                {
                    "node": "2.1.3",
                    "distance": 21394
                },
                {
                    "node": "2.1.4",
                    "distance": 21394
                },
                {
                    "node": "2.2.1",
                    "distance": 18222
                },
                {
                    "node": "2.2.2",
                    "distance": 18222
                },
                {
                    "node": "2.2.3",
                    "distance": 18222
                },
                {
                    "node": "2.2.4",
                    "distance": 18222
                },
                {
                    "node": "2.3.1",
                    "distance": 16752
                },
                {
                    "node": "2.3.2",
                    "distance": 16752
                },
                {
                    "node": "2.3.3",
                    "distance": 16752
                },
                {
                    "node": "2.3.4",
                    "distance": 16752
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "2.6": [
                {
                    "node": "1.1.1",
                    "distance": 21130
                },
                {
                    "node": "1.1.2",
                    "distance": 21130
                },
                {
                    "node": "1.1.3",
                    "distance": 21130
                },
                {
                    "node": "1.1.4",
                    "distance": 21130
                },
                {
                    "node": "1.2.1",
                    "distance": 17958
                },
                {
                    "node": "1.2.2",
                    "distance": 17958
                },
                {
                    "node": "1.2.3",
                    "distance": 17958
                },
                {
                    "node": "1.2.4",
                    "distance": 17958
                },
                {
                    "node": "1.3.1",
                    "distance": 16776
                },
                {
                    "node": "1.3.2",
                    "distance": 16776
                },
                {
                    "node": "1.3.3",
                    "distance": 16776
                },
                {
                    "node": "1.3.4",
                    "distance": 16776
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 21394
                },
                {
                    "node": "2.1.2",
                    "distance": 21394
                },
                {
                    "node": "2.1.3",
                    "distance": 21394
                },
                {
                    "node": "2.1.4",
                    "distance": 21394
                },
                {
                    "node": "2.2.1",
                    "distance": 18222
                },
                {
                    "node": "2.2.2",
                    "distance": 18222
                },
                {
                    "node": "2.2.3",
                    "distance": 18222
                },
                {
                    "node": "2.2.4",
                    "distance": 18222
                },
                {
                    "node": "2.3.1",
                    "distance": 16752
                },
                {
                    "node": "2.3.2",
                    "distance": 16752
                },
                {
                    "node": "2.3.3",
                    "distance": 16752
                },
                {
                    "node": "2.3.4",
                    "distance": 16752
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "3.1": [
                {
                    "node": "1.1.1",
                    "distance": 21130
                },
                {
                    "node": "1.1.2",
                    "distance": 21130
                },
                {
                    "node": "1.1.3",
                    "distance": 21130
                },
                {
                    "node": "1.1.4",
                    "distance": 21130
                },
                {
                    "node": "1.2.1",
                    "distance": 17958
                },
                {
                    "node": "1.2.2",
                    "distance": 17958
                },
                {
                    "node": "1.2.3",
                    "distance": 17958
                },
                {
                    "node": "1.2.4",
                    "distance": 17958
                },
                {
                    "node": "1.3.1",
                    "distance": 16776
                },
                {
                    "node": "1.3.2",
                    "distance": 16776
                },
                {
                    "node": "1.3.3",
                    "distance": 16776
                },
                {
                    "node": "1.3.4",
                    "distance": 16776
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 21394
                },
                {
                    "node": "2.1.2",
                    "distance": 21394
                },
                {
                    "node": "2.1.3",
                    "distance": 21394
                },
                {
                    "node": "2.1.4",
                    "distance": 21394
                },
                {
                    "node": "2.2.1",
                    "distance": 18222
                },
                {
                    "node": "2.2.2",
                    "distance": 18222
                },
                {
                    "node": "2.2.3",
                    "distance": 18222
                },
                {
                    "node": "2.2.4",
                    "distance": 18222
                },
                {
                    "node": "2.3.1",
                    "distance": 16752
                },
                {
                    "node": "2.3.2",
                    "distance": 16752
                },
                {
                    "node": "2.3.3",
                    "distance": 16752
                },
                {
                    "node": "2.3.4",
                    "distance": 16752
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "3.2": [
                {
                    "node": "1.1.1",
                    "distance": 21130
                },
                {
                    "node": "1.1.2",
                    "distance": 21130
                },
                {
                    "node": "1.1.3",
                    "distance": 21130
                },
                {
                    "node": "1.1.4",
                    "distance": 21130
                },
                {
                    "node": "1.2.1",
                    "distance": 17958
                },
                {
                    "node": "1.2.2",
                    "distance": 17958
                },
                {
                    "node": "1.2.3",
                    "distance": 17958
                },
                {
                    "node": "1.2.4",
                    "distance": 17958
                },
                {
                    "node": "1.3.1",
                    "distance": 16776
                },
                {
                    "node": "1.3.2",
                    "distance": 16776
                },
                {
                    "node": "1.3.3",
                    "distance": 16776
                },
                {
                    "node": "1.3.4",
                    "distance": 16776
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 21394
                },
                {
                    "node": "2.1.2",
                    "distance": 21394
                },
                {
                    "node": "2.1.3",
                    "distance": 21394
                },
                {
                    "node": "2.1.4",
                    "distance": 21394
                },
                {
                    "node": "2.2.1",
                    "distance": 18222
                },
                {
                    "node": "2.2.2",
                    "distance": 18222
                },
                {
                    "node": "2.2.3",
                    "distance": 18222
                },
                {
                    "node": "2.2.4",
                    "distance": 18222
                },
                {
                    "node": "2.3.1",
                    "distance": 16752
                },
                {
                    "node": "2.3.2",
                    "distance": 16752
                },
                {
                    "node": "2.3.3",
                    "distance": 16752
                },
                {
                    "node": "2.3.4",
                    "distance": 16752
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "3.3": [
                {
                    "node": "1.1.1",
                    "distance": 21130
                },
                {
                    "node": "1.1.2",
                    "distance": 21130
                },
                {
                    "node": "1.1.3",
                    "distance": 21130
                },
                {
                    "node": "1.1.4",
                    "distance": 21130
                },
                {
                    "node": "1.2.1",
                    "distance": 17958
                },
                {
                    "node": "1.2.2",
                    "distance": 17958
                },
                {
                    "node": "1.2.3",
                    "distance": 17958
                },
                {
                    "node": "1.2.4",
                    "distance": 17958
                },
                {
                    "node": "1.3.1",
                    "distance": 16776
                },
                {
                    "node": "1.3.2",
                    "distance": 16776
                },
                {
                    "node": "1.3.3",
                    "distance": 16776
                },
                {
                    "node": "1.3.4",
                    "distance": 16776
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 21394
                },
                {
                    "node": "2.1.2",
                    "distance": 21394
                },
                {
                    "node": "2.1.3",
                    "distance": 21394
                },
                {
                    "node": "2.1.4",
                    "distance": 21394
                },
                {
                    "node": "2.2.1",
                    "distance": 18222
                },
                {
                    "node": "2.2.2",
                    "distance": 18222
                },
                {
                    "node": "2.2.3",
                    "distance": 18222
                },
                {
                    "node": "2.2.4",
                    "distance": 18222
                },
                {
                    "node": "2.3.1",
                    "distance": 16752
                },
                {
                    "node": "2.3.2",
                    "distance": 16752
                },
                {
                    "node": "2.3.3",
                    "distance": 16752
                },
                {
                    "node": "2.3.4",
                    "distance": 16752
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "3.4": [
                {
                    "node": "1.1.1",
                    "distance": 27570
                },
                {
                    "node": "1.1.2",
                    "distance": 27570
                },
                {
                    "node": "1.1.3",
                    "distance": 27570
                },
                {
                    "node": "1.1.4",
                    "distance": 27570
                },
                {
                    "node": "1.2.1",
                    "distance": 24329
                },
                {
                    "node": "1.2.2",
                    "distance": 24329
                },
                {
                    "node": "1.2.3",
                    "distance": 24329
                },
                {
                    "node": "1.2.4",
                    "distance": 24329
                },
                {
                    "node": "1.3.1",
                    "distance": 21130
                },
                {
                    "node": "1.3.2",
                    "distance": 21130
                },
                {
                    "node": "1.3.3",
                    "distance": 21130
                },
                {
                    "node": "1.3.4",
                    "distance": 21130
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 27834
                },
                {
                    "node": "2.1.2",
                    "distance": 27834
                },
                {
                    "node": "2.1.3",
                    "distance": 27834
                },
                {
                    "node": "2.1.4",
                    "distance": 27834
                },
                {
                    "node": "2.2.1",
                    "distance": 24593
                },
                {
                    "node": "2.2.2",
                    "distance": 24593
                },
                {
                    "node": "2.2.3",
                    "distance": 24593
                },
                {
                    "node": "2.2.4",
                    "distance": 24593
                },
                {
                    "node": "2.3.1",
                    "distance": 21394
                },
                {
                    "node": "2.3.2",
                    "distance": 21394
                },
                {
                    "node": "2.3.3",
                    "distance": 21394
                },
                {
                    "node": "2.3.4",
                    "distance": 21394
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "3.5": [
                {
                    "node": "1.1.1",
                    "distance": 27570
                },
                {
                    "node": "1.1.2",
                    "distance": 27570
                },
                {
                    "node": "1.1.3",
                    "distance": 27570
                },
                {
                    "node": "1.1.4",
                    "distance": 27570
                },
                {
                    "node": "1.2.1",
                    "distance": 24329
                },
                {
                    "node": "1.2.2",
                    "distance": 24329
                },
                {
                    "node": "1.2.3",
                    "distance": 24329
                },
                {
                    "node": "1.2.4",
                    "distance": 24329
                },
                {
                    "node": "1.3.1",
                    "distance": 21130
                },
                {
                    "node": "1.3.2",
                    "distance": 21130
                },
                {
                    "node": "1.3.3",
                    "distance": 21130
                },
                {
                    "node": "1.3.4",
                    "distance": 21130
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 27834
                },
                {
                    "node": "2.1.2",
                    "distance": 27834
                },
                {
                    "node": "2.1.3",
                    "distance": 27834
                },
                {
                    "node": "2.1.4",
                    "distance": 27834
                },
                {
                    "node": "2.2.1",
                    "distance": 24593
                },
                {
                    "node": "2.2.2",
                    "distance": 24593
                },
                {
                    "node": "2.2.3",
                    "distance": 24593
                },
                {
                    "node": "2.2.4",
                    "distance": 24593
                },
                {
                    "node": "2.3.1",
                    "distance": 21394
                },
                {
                    "node": "2.3.2",
                    "distance": 21394
                },
                {
                    "node": "2.3.3",
                    "distance": 21394
                },
                {
                    "node": "2.3.4",
                    "distance": 21394
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "3.6": [
                {
                    "node": "1.1.1",
                    "distance": 27570
                },
                {
                    "node": "1.1.2",
                    "distance": 27570
                },
                {
                    "node": "1.1.3",
                    "distance": 27570
                },
                {
                    "node": "1.1.4",
                    "distance": 27570
                },
                {
                    "node": "1.2.1",
                    "distance": 24329
                },
                {
                    "node": "1.2.2",
                    "distance": 24329
                },
                {
                    "node": "1.2.3",
                    "distance": 24329
                },
                {
                    "node": "1.2.4",
                    "distance": 24329
                },
                {
                    "node": "1.3.1",
                    "distance": 21130
                },
                {
                    "node": "1.3.2",
                    "distance": 21130
                },
                {
                    "node": "1.3.3",
                    "distance": 21130
                },
                {
                    "node": "1.3.4",
                    "distance": 21130
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 27834
                },
                {
                    "node": "2.1.2",
                    "distance": 27834
                },
                {
                    "node": "2.1.3",
                    "distance": 27834
                },
                {
                    "node": "2.1.4",
                    "distance": 27834
                },
                {
                    "node": "2.2.1",
                    "distance": 24593
                },
                {
                    "node": "2.2.2",
                    "distance": 24593
                },
                {
                    "node": "2.2.3",
                    "distance": 24593
                },
                {
                    "node": "2.2.4",
                    "distance": 24593
                },
                {
                    "node": "2.3.1",
                    "distance": 21394
                },
                {
                    "node": "2.3.2",
                    "distance": 21394
                },
                {
                    "node": "2.3.3",
                    "distance": 21394
                },
                {
                    "node": "2.3.4",
                    "distance": 21394
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "4.1": [
                {
                    "node": "1.1.1",
                    "distance": 27570
                },
                {
                    "node": "1.1.2",
                    "distance": 27570
                },
                {
                    "node": "1.1.3",
                    "distance": 27570
                },
                {
                    "node": "1.1.4",
                    "distance": 27570
                },
                {
                    "node": "1.2.1",
                    "distance": 24329
                },
                {
                    "node": "1.2.2",
                    "distance": 24329
                },
                {
                    "node": "1.2.3",
                    "distance": 24329
                },
                {
                    "node": "1.2.4",
                    "distance": 24329
                },
                {
                    "node": "1.3.1",
                    "distance": 21130
                },
                {
                    "node": "1.3.2",
                    "distance": 21130
                },
                {
                    "node": "1.3.3",
                    "distance": 21130
                },
                {
                    "node": "1.3.4",
                    "distance": 21130
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 27834
                },
                {
                    "node": "2.1.2",
                    "distance": 27834
                },
                {
                    "node": "2.1.3",
                    "distance": 27834
                },
                {
                    "node": "2.1.4",
                    "distance": 27834
                },
                {
                    "node": "2.2.1",
                    "distance": 24593
                },
                {
                    "node": "2.2.2",
                    "distance": 24593
                },
                {
                    "node": "2.2.3",
                    "distance": 24593
                },
                {
                    "node": "2.2.4",
                    "distance": 24593
                },
                {
                    "node": "2.3.1",
                    "distance": 21394
                },
                {
                    "node": "2.3.2",
                    "distance": 21394
                },
                {
                    "node": "2.3.3",
                    "distance": 21394
                },
                {
                    "node": "2.3.4",
                    "distance": 21394
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "4.2": [
                {
                    "node": "1.1.1",
                    "distance": 27570
                },
                {
                    "node": "1.1.2",
                    "distance": 27570
                },
                {
                    "node": "1.1.3",
                    "distance": 27570
                },
                {
                    "node": "1.1.4",
                    "distance": 27570
                },
                {
                    "node": "1.2.1",
                    "distance": 24329
                },
                {
                    "node": "1.2.2",
                    "distance": 24329
                },
                {
                    "node": "1.2.3",
                    "distance": 24329
                },
                {
                    "node": "1.2.4",
                    "distance": 24329
                },
                {
                    "node": "1.3.1",
                    "distance": 21130
                },
                {
                    "node": "1.3.2",
                    "distance": 21130
                },
                {
                    "node": "1.3.3",
                    "distance": 21130
                },
                {
                    "node": "1.3.4",
                    "distance": 21130
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 27834
                },
                {
                    "node": "2.1.2",
                    "distance": 27834
                },
                {
                    "node": "2.1.3",
                    "distance": 27834
                },
                {
                    "node": "2.1.4",
                    "distance": 27834
                },
                {
                    "node": "2.2.1",
                    "distance": 24593
                },
                {
                    "node": "2.2.2",
                    "distance": 24593
                },
                {
                    "node": "2.2.3",
                    "distance": 24593
                },
                {
                    "node": "2.2.4",
                    "distance": 24593
                },
                {
                    "node": "2.3.1",
                    "distance": 21394
                },
                {
                    "node": "2.3.2",
                    "distance": 21394
                },
                {
                    "node": "2.3.3",
                    "distance": 21394
                },
                {
                    "node": "2.3.4",
                    "distance": 21394
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "4.3": [
                {
                    "node": "1.1.1",
                    "distance": 27570
                },
                {
                    "node": "1.1.2",
                    "distance": 27570
                },
                {
                    "node": "1.1.3",
                    "distance": 27570
                },
                {
                    "node": "1.1.4",
                    "distance": 27570
                },
                {
                    "node": "1.2.1",
                    "distance": 24329
                },
                {
                    "node": "1.2.2",
                    "distance": 24329
                },
                {
                    "node": "1.2.3",
                    "distance": 24329
                },
                {
                    "node": "1.2.4",
                    "distance": 24329
                },
                {
                    "node": "1.3.1",
                    "distance": 21130
                },
                {
                    "node": "1.3.2",
                    "distance": 21130
                },
                {
                    "node": "1.3.3",
                    "distance": 21130
                },
                {
                    "node": "1.3.4",
                    "distance": 21130
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 27834
                },
                {
                    "node": "2.1.2",
                    "distance": 27834
                },
                {
                    "node": "2.1.3",
                    "distance": 27834
                },
                {
                    "node": "2.1.4",
                    "distance": 27834
                },
                {
                    "node": "2.2.1",
                    "distance": 24593
                },
                {
                    "node": "2.2.2",
                    "distance": 24593
                },
                {
                    "node": "2.2.3",
                    "distance": 24593
                },
                {
                    "node": "2.2.4",
                    "distance": 24593
                },
                {
                    "node": "2.3.1",
                    "distance": 21394
                },
                {
                    "node": "2.3.2",
                    "distance": 21394
                },
                {
                    "node": "2.3.3",
                    "distance": 21394
                },
                {
                    "node": "2.3.4",
                    "distance": 21394
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "4.4": [
                {
                    "node": "1.1.1",
                    "distance": 27570
                },
                {
                    "node": "1.1.2",
                    "distance": 27570
                },
                {
                    "node": "1.1.3",
                    "distance": 27570
                },
                {
                    "node": "1.1.4",
                    "distance": 27570
                },
                {
                    "node": "1.2.1",
                    "distance": 24329
                },
                {
                    "node": "1.2.2",
                    "distance": 24329
                },
                {
                    "node": "1.2.3",
                    "distance": 24329
                },
                {
                    "node": "1.2.4",
                    "distance": 24329
                },
                {
                    "node": "1.3.1",
                    "distance": 21130
                },
                {
                    "node": "1.3.2",
                    "distance": 21130
                },
                {
                    "node": "1.3.3",
                    "distance": 21130
                },
                {
                    "node": "1.3.4",
                    "distance": 21130
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 27834
                },
                {
                    "node": "2.1.2",
                    "distance": 27834
                },
                {
                    "node": "2.1.3",
                    "distance": 27834
                },
                {
                    "node": "2.1.4",
                    "distance": 27834
                },
                {
                    "node": "2.2.1",
                    "distance": 24593
                },
                {
                    "node": "2.2.2",
                    "distance": 24593
                },
                {
                    "node": "2.2.3",
                    "distance": 24593
                },
                {
                    "node": "2.2.4",
                    "distance": 24593
                },
                {
                    "node": "2.3.1",
                    "distance": 21394
                },
                {
                    "node": "2.3.2",
                    "distance": 21394
                },
                {
                    "node": "2.3.3",
                    "distance": 21394
                },
                {
                    "node": "2.3.4",
                    "distance": 21394
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "4.5": [
                {
                    "node": "1.1.1",
                    "distance": 27570
                },
                {
                    "node": "1.1.2",
                    "distance": 27570
                },
                {
                    "node": "1.1.3",
                    "distance": 27570
                },
                {
                    "node": "1.1.4",
                    "distance": 27570
                },
                {
                    "node": "1.2.1",
                    "distance": 24329
                },
                {
                    "node": "1.2.2",
                    "distance": 24329
                },
                {
                    "node": "1.2.3",
                    "distance": 24329
                },
                {
                    "node": "1.2.4",
                    "distance": 24329
                },
                {
                    "node": "1.3.1",
                    "distance": 21130
                },
                {
                    "node": "1.3.2",
                    "distance": 21130
                },
                {
                    "node": "1.3.3",
                    "distance": 21130
                },
                {
                    "node": "1.3.4",
                    "distance": 21130
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 27834
                },
                {
                    "node": "2.1.2",
                    "distance": 27834
                },
                {
                    "node": "2.1.3",
                    "distance": 27834
                },
                {
                    "node": "2.1.4",
                    "distance": 27834
                },
                {
                    "node": "2.2.1",
                    "distance": 24593
                },
                {
                    "node": "2.2.2",
                    "distance": 24593
                },
                {
                    "node": "2.2.3",
                    "distance": 24593
                },
                {
                    "node": "2.2.4",
                    "distance": 24593
                },
                {
                    "node": "2.3.1",
                    "distance": 21394
                },
                {
                    "node": "2.3.2",
                    "distance": 21394
                },
                {
                    "node": "2.3.3",
                    "distance": 21394
                },
                {
                    "node": "2.3.4",
                    "distance": 21394
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "4.6": [
                {
                    "node": "1.1.1",
                    "distance": 27570
                },
                {
                    "node": "1.1.2",
                    "distance": 27570
                },
                {
                    "node": "1.1.3",
                    "distance": 27570
                },
                {
                    "node": "1.1.4",
                    "distance": 27570
                },
                {
                    "node": "1.2.1",
                    "distance": 24329
                },
                {
                    "node": "1.2.2",
                    "distance": 24329
                },
                {
                    "node": "1.2.3",
                    "distance": 24329
                },
                {
                    "node": "1.2.4",
                    "distance": 24329
                },
                {
                    "node": "1.3.1",
                    "distance": 21130
                },
                {
                    "node": "1.3.2",
                    "distance": 21130
                },
                {
                    "node": "1.3.3",
                    "distance": 21130
                },
                {
                    "node": "1.3.4",
                    "distance": 21130
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 27834
                },
                {
                    "node": "2.1.2",
                    "distance": 27834
                },
                {
                    "node": "2.1.3",
                    "distance": 27834
                },
                {
                    "node": "2.1.4",
                    "distance": 27834
                },
                {
                    "node": "2.2.1",
                    "distance": 24593
                },
                {
                    "node": "2.2.2",
                    "distance": 24593
                },
                {
                    "node": "2.2.3",
                    "distance": 24593
                },
                {
                    "node": "2.2.4",
                    "distance": 24593
                },
                {
                    "node": "2.3.1",
                    "distance": 21394
                },
                {
                    "node": "2.3.2",
                    "distance": 21394
                },
                {
                    "node": "2.3.3",
                    "distance": 21394
                },
                {
                    "node": "2.3.4",
                    "distance": 21394
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        }
    ],
    "1.1": [
        {
            "1.1": [
                {
                    "node": "1.1.1",
                    "distance": 18522
                },
                {
                    "node": "1.1.2",
                    "distance": 18522
                },
                {
                    "node": "1.1.3",
                    "distance": 18522
                },
                {
                    "node": "1.1.4",
                    "distance": 18522
                },
                {
                    "node": "1.2.1",
                    "distance": 18522
                },
                {
                    "node": "1.2.2",
                    "distance": 18522
                },
                {
                    "node": "1.2.3",
                    "distance": 18522
                },
                {
                    "node": "1.2.4",
                    "distance": 18522
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 27230
                },
                {
                    "node": "1.5.2",
                    "distance": 27230
                },
                {
                    "node": "1.5.3",
                    "distance": 27230
                },
                {
                    "node": "1.5.4",
                    "distance": 27230
                },
                {
                    "node": "1.6.1",
                    "distance": 33628
                },
                {
                    "node": "1.6.2",
                    "distance": 33628
                },
                {
                    "node": "1.6.3",
                    "distance": 33628
                },
                {
                    "node": "1.6.4",
                    "distance": 33628
                },
                {
                    "node": "1.7.1",
                    "distance": 40110
                },
                {
                    "node": "1.7.2",
                    "distance": 40110
                },
                {
                    "node": "1.7.3",
                    "distance": 40110
                },
                {
                    "node": "1.7.4",
                    "distance": 40110
                },
                {
                    "node": "2.1.1",
                    "distance": 17946
                },
                {
                    "node": "2.1.2",
                    "distance": 17946
                },
                {
                    "node": "2.1.3",
                    "distance": 17946
                },
                {
                    "node": "2.1.4",
                    "distance": 17946
                },
                {
                    "node": "2.2.1",
                    "distance": 17946
                },
                {
                    "node": "2.2.2",
                    "distance": 17946
                },
                {
                    "node": "2.2.3",
                    "distance": 17946
                },
                {
                    "node": "2.2.4",
                    "distance": 17946
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 27230
                },
                {
                    "node": "2.5.2",
                    "distance": 27230
                },
                {
                    "node": "2.5.3",
                    "distance": 27230
                },
                {
                    "node": "2.5.4",
                    "distance": 27230
                },
                {
                    "node": "2.6.1",
                    "distance": 33628
                },
                {
                    "node": "2.6.2",
                    "distance": 33628
                },
                {
                    "node": "2.6.3",
                    "distance": 33628
                },
                {
                    "node": "2.6.4",
                    "distance": 33628
                },
                {
                    "node": "2.7.1",
                    "distance": 40110
                },
                {
                    "node": "2.7.2",
                    "distance": 40110
                },
                {
                    "node": "2.7.3",
                    "distance": 40110
                },
                {
                    "node": "2.7.4",
                    "distance": 40110
                }
            ]
        },
        {
            "1.2": [
                {
                    "node": "1.1.1",
                    "distance": 18522
                },
                {
                    "node": "1.1.2",
                    "distance": 18522
                },
                {
                    "node": "1.1.3",
                    "distance": 18522
                },
                {
                    "node": "1.1.4",
                    "distance": 18522
                },
                {
                    "node": "1.2.1",
                    "distance": 18522
                },
                {
                    "node": "1.2.2",
                    "distance": 18522
                },
                {
                    "node": "1.2.3",
                    "distance": 18522
                },
                {
                    "node": "1.2.4",
                    "distance": 18522
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 27230
                },
                {
                    "node": "1.5.2",
                    "distance": 27230
                },
                {
                    "node": "1.5.3",
                    "distance": 27230
                },
                {
                    "node": "1.5.4",
                    "distance": 27230
                },
                {
                    "node": "1.6.1",
                    "distance": 33628
                },
                {
                    "node": "1.6.2",
                    "distance": 33628
                },
                {
                    "node": "1.6.3",
                    "distance": 33628
                },
                {
                    "node": "1.6.4",
                    "distance": 33628
                },
                {
                    "node": "1.7.1",
                    "distance": 40110
                },
                {
                    "node": "1.7.2",
                    "distance": 40110
                },
                {
                    "node": "1.7.3",
                    "distance": 40110
                },
                {
                    "node": "1.7.4",
                    "distance": 40110
                },
                {
                    "node": "2.1.1",
                    "distance": 17946
                },
                {
                    "node": "2.1.2",
                    "distance": 17946
                },
                {
                    "node": "2.1.3",
                    "distance": 17946
                },
                {
                    "node": "2.1.4",
                    "distance": 17946
                },
                {
                    "node": "2.2.1",
                    "distance": 17946
                },
                {
                    "node": "2.2.2",
                    "distance": 17946
                },
                {
                    "node": "2.2.3",
                    "distance": 17946
                },
                {
                    "node": "2.2.4",
                    "distance": 17946
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 27230
                },
                {
                    "node": "2.5.2",
                    "distance": 27230
                },
                {
                    "node": "2.5.3",
                    "distance": 27230
                },
                {
                    "node": "2.5.4",
                    "distance": 27230
                },
                {
                    "node": "2.6.1",
                    "distance": 33628
                },
                {
                    "node": "2.6.2",
                    "distance": 33628
                },
                {
                    "node": "2.6.3",
                    "distance": 33628
                },
                {
                    "node": "2.6.4",
                    "distance": 33628
                },
                {
                    "node": "2.7.1",
                    "distance": 40110
                },
                {
                    "node": "2.7.2",
                    "distance": 40110
                },
                {
                    "node": "2.7.3",
                    "distance": 40110
                },
                {
                    "node": "2.7.4",
                    "distance": 40110
                }
            ]
        },
        {
            "1.3": [
                {
                    "node": "1.1.1",
                    "distance": 18522
                },
                {
                    "node": "1.1.2",
                    "distance": 18522
                },
                {
                    "node": "1.1.3",
                    "distance": 18522
                },
                {
                    "node": "1.1.4",
                    "distance": 18522
                },
                {
                    "node": "1.2.1",
                    "distance": 18522
                },
                {
                    "node": "1.2.2",
                    "distance": 18522
                },
                {
                    "node": "1.2.3",
                    "distance": 18522
                },
                {
                    "node": "1.2.4",
                    "distance": 18522
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 27230
                },
                {
                    "node": "1.5.2",
                    "distance": 27230
                },
                {
                    "node": "1.5.3",
                    "distance": 27230
                },
                {
                    "node": "1.5.4",
                    "distance": 27230
                },
                {
                    "node": "1.6.1",
                    "distance": 33628
                },
                {
                    "node": "1.6.2",
                    "distance": 33628
                },
                {
                    "node": "1.6.3",
                    "distance": 33628
                },
                {
                    "node": "1.6.4",
                    "distance": 33628
                },
                {
                    "node": "1.7.1",
                    "distance": 40110
                },
                {
                    "node": "1.7.2",
                    "distance": 40110
                },
                {
                    "node": "1.7.3",
                    "distance": 40110
                },
                {
                    "node": "1.7.4",
                    "distance": 40110
                },
                {
                    "node": "2.1.1",
                    "distance": 17946
                },
                {
                    "node": "2.1.2",
                    "distance": 17946
                },
                {
                    "node": "2.1.3",
                    "distance": 17946
                },
                {
                    "node": "2.1.4",
                    "distance": 17946
                },
                {
                    "node": "2.2.1",
                    "distance": 17946
                },
                {
                    "node": "2.2.2",
                    "distance": 17946
                },
                {
                    "node": "2.2.3",
                    "distance": 17946
                },
                {
                    "node": "2.2.4",
                    "distance": 17946
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 27230
                },
                {
                    "node": "2.5.2",
                    "distance": 27230
                },
                {
                    "node": "2.5.3",
                    "distance": 27230
                },
                {
                    "node": "2.5.4",
                    "distance": 27230
                },
                {
                    "node": "2.6.1",
                    "distance": 33628
                },
                {
                    "node": "2.6.2",
                    "distance": 33628
                },
                {
                    "node": "2.6.3",
                    "distance": 33628
                },
                {
                    "node": "2.6.4",
                    "distance": 33628
                },
                {
                    "node": "2.7.1",
                    "distance": 40110
                },
                {
                    "node": "2.7.2",
                    "distance": 40110
                },
                {
                    "node": "2.7.3",
                    "distance": 40110
                },
                {
                    "node": "2.7.4",
                    "distance": 40110
                }
            ]
        },
        {
            "1.4": [
                {
                    "node": "1.1.1",
                    "distance": 18522
                },
                {
                    "node": "1.1.2",
                    "distance": 18522
                },
                {
                    "node": "1.1.3",
                    "distance": 18522
                },
                {
                    "node": "1.1.4",
                    "distance": 18522
                },
                {
                    "node": "1.2.1",
                    "distance": 18522
                },
                {
                    "node": "1.2.2",
                    "distance": 18522
                },
                {
                    "node": "1.2.3",
                    "distance": 18522
                },
                {
                    "node": "1.2.4",
                    "distance": 18522
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 27230
                },
                {
                    "node": "1.5.2",
                    "distance": 27230
                },
                {
                    "node": "1.5.3",
                    "distance": 27230
                },
                {
                    "node": "1.5.4",
                    "distance": 27230
                },
                {
                    "node": "1.6.1",
                    "distance": 33628
                },
                {
                    "node": "1.6.2",
                    "distance": 33628
                },
                {
                    "node": "1.6.3",
                    "distance": 33628
                },
                {
                    "node": "1.6.4",
                    "distance": 33628
                },
                {
                    "node": "1.7.1",
                    "distance": 40110
                },
                {
                    "node": "1.7.2",
                    "distance": 40110
                },
                {
                    "node": "1.7.3",
                    "distance": 40110
                },
                {
                    "node": "1.7.4",
                    "distance": 40110
                },
                {
                    "node": "2.1.1",
                    "distance": 17946
                },
                {
                    "node": "2.1.2",
                    "distance": 17946
                },
                {
                    "node": "2.1.3",
                    "distance": 17946
                },
                {
                    "node": "2.1.4",
                    "distance": 17946
                },
                {
                    "node": "2.2.1",
                    "distance": 17946
                },
                {
                    "node": "2.2.2",
                    "distance": 17946
                },
                {
                    "node": "2.2.3",
                    "distance": 17946
                },
                {
                    "node": "2.2.4",
                    "distance": 17946
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 27230
                },
                {
                    "node": "2.5.2",
                    "distance": 27230
                },
                {
                    "node": "2.5.3",
                    "distance": 27230
                },
                {
                    "node": "2.5.4",
                    "distance": 27230
                },
                {
                    "node": "2.6.1",
                    "distance": 33628
                },
                {
                    "node": "2.6.2",
                    "distance": 33628
                },
                {
                    "node": "2.6.3",
                    "distance": 33628
                },
                {
                    "node": "2.6.4",
                    "distance": 33628
                },
                {
                    "node": "2.7.1",
                    "distance": 40110
                },
                {
                    "node": "2.7.2",
                    "distance": 40110
                },
                {
                    "node": "2.7.3",
                    "distance": 40110
                },
                {
                    "node": "2.7.4",
                    "distance": 40110
                }
            ]
        },
        {
            "1.5": [
                {
                    "node": "1.1.1",
                    "distance": 18522
                },
                {
                    "node": "1.1.2",
                    "distance": 18522
                },
                {
                    "node": "1.1.3",
                    "distance": 18522
                },
                {
                    "node": "1.1.4",
                    "distance": 18522
                },
                {
                    "node": "1.2.1",
                    "distance": 18522
                },
                {
                    "node": "1.2.2",
                    "distance": 18522
                },
                {
                    "node": "1.2.3",
                    "distance": 18522
                },
                {
                    "node": "1.2.4",
                    "distance": 18522
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 27230
                },
                {
                    "node": "1.5.2",
                    "distance": 27230
                },
                {
                    "node": "1.5.3",
                    "distance": 27230
                },
                {
                    "node": "1.5.4",
                    "distance": 27230
                },
                {
                    "node": "1.6.1",
                    "distance": 33628
                },
                {
                    "node": "1.6.2",
                    "distance": 33628
                },
                {
                    "node": "1.6.3",
                    "distance": 33628
                },
                {
                    "node": "1.6.4",
                    "distance": 33628
                },
                {
                    "node": "1.7.1",
                    "distance": 40110
                },
                {
                    "node": "1.7.2",
                    "distance": 40110
                },
                {
                    "node": "1.7.3",
                    "distance": 40110
                },
                {
                    "node": "1.7.4",
                    "distance": 40110
                },
                {
                    "node": "2.1.1",
                    "distance": 17946
                },
                {
                    "node": "2.1.2",
                    "distance": 17946
                },
                {
                    "node": "2.1.3",
                    "distance": 17946
                },
                {
                    "node": "2.1.4",
                    "distance": 17946
                },
                {
                    "node": "2.2.1",
                    "distance": 17946
                },
                {
                    "node": "2.2.2",
                    "distance": 17946
                },
                {
                    "node": "2.2.3",
                    "distance": 17946
                },
                {
                    "node": "2.2.4",
                    "distance": 17946
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 27230
                },
                {
                    "node": "2.5.2",
                    "distance": 27230
                },
                {
                    "node": "2.5.3",
                    "distance": 27230
                },
                {
                    "node": "2.5.4",
                    "distance": 27230
                },
                {
                    "node": "2.6.1",
                    "distance": 33628
                },
                {
                    "node": "2.6.2",
                    "distance": 33628
                },
                {
                    "node": "2.6.3",
                    "distance": 33628
                },
                {
                    "node": "2.6.4",
                    "distance": 33628
                },
                {
                    "node": "2.7.1",
                    "distance": 40110
                },
                {
                    "node": "2.7.2",
                    "distance": 40110
                },
                {
                    "node": "2.7.3",
                    "distance": 40110
                },
                {
                    "node": "2.7.4",
                    "distance": 40110
                }
            ]
        },
        {
            "1.6": [
                {
                    "node": "1.1.1",
                    "distance": 18522
                },
                {
                    "node": "1.1.2",
                    "distance": 18522
                },
                {
                    "node": "1.1.3",
                    "distance": 18522
                },
                {
                    "node": "1.1.4",
                    "distance": 18522
                },
                {
                    "node": "1.2.1",
                    "distance": 18522
                },
                {
                    "node": "1.2.2",
                    "distance": 18522
                },
                {
                    "node": "1.2.3",
                    "distance": 18522
                },
                {
                    "node": "1.2.4",
                    "distance": 18522
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 27230
                },
                {
                    "node": "1.5.2",
                    "distance": 27230
                },
                {
                    "node": "1.5.3",
                    "distance": 27230
                },
                {
                    "node": "1.5.4",
                    "distance": 27230
                },
                {
                    "node": "1.6.1",
                    "distance": 33628
                },
                {
                    "node": "1.6.2",
                    "distance": 33628
                },
                {
                    "node": "1.6.3",
                    "distance": 33628
                },
                {
                    "node": "1.6.4",
                    "distance": 33628
                },
                {
                    "node": "1.7.1",
                    "distance": 40110
                },
                {
                    "node": "1.7.2",
                    "distance": 40110
                },
                {
                    "node": "1.7.3",
                    "distance": 40110
                },
                {
                    "node": "1.7.4",
                    "distance": 40110
                },
                {
                    "node": "2.1.1",
                    "distance": 17946
                },
                {
                    "node": "2.1.2",
                    "distance": 17946
                },
                {
                    "node": "2.1.3",
                    "distance": 17946
                },
                {
                    "node": "2.1.4",
                    "distance": 17946
                },
                {
                    "node": "2.2.1",
                    "distance": 17946
                },
                {
                    "node": "2.2.2",
                    "distance": 17946
                },
                {
                    "node": "2.2.3",
                    "distance": 17946
                },
                {
                    "node": "2.2.4",
                    "distance": 17946
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 27230
                },
                {
                    "node": "2.5.2",
                    "distance": 27230
                },
                {
                    "node": "2.5.3",
                    "distance": 27230
                },
                {
                    "node": "2.5.4",
                    "distance": 27230
                },
                {
                    "node": "2.6.1",
                    "distance": 33628
                },
                {
                    "node": "2.6.2",
                    "distance": 33628
                },
                {
                    "node": "2.6.3",
                    "distance": 33628
                },
                {
                    "node": "2.6.4",
                    "distance": 33628
                },
                {
                    "node": "2.7.1",
                    "distance": 40110
                },
                {
                    "node": "2.7.2",
                    "distance": 40110
                },
                {
                    "node": "2.7.3",
                    "distance": 40110
                },
                {
                    "node": "2.7.4",
                    "distance": 40110
                }
            ]
        },
        {
            "2.1": [
                {
                    "node": "1.1.1",
                    "distance": 18522
                },
                {
                    "node": "1.1.2",
                    "distance": 18522
                },
                {
                    "node": "1.1.3",
                    "distance": 18522
                },
                {
                    "node": "1.1.4",
                    "distance": 18522
                },
                {
                    "node": "1.2.1",
                    "distance": 18522
                },
                {
                    "node": "1.2.2",
                    "distance": 18522
                },
                {
                    "node": "1.2.3",
                    "distance": 18522
                },
                {
                    "node": "1.2.4",
                    "distance": 18522
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 27257
                },
                {
                    "node": "1.6.2",
                    "distance": 27257
                },
                {
                    "node": "1.6.3",
                    "distance": 27257
                },
                {
                    "node": "1.6.4",
                    "distance": 27257
                },
                {
                    "node": "1.7.1",
                    "distance": 33670
                },
                {
                    "node": "1.7.2",
                    "distance": 33670
                },
                {
                    "node": "1.7.3",
                    "distance": 33670
                },
                {
                    "node": "1.7.4",
                    "distance": 33670
                },
                {
                    "node": "2.1.1",
                    "distance": 17946
                },
                {
                    "node": "2.1.2",
                    "distance": 17946
                },
                {
                    "node": "2.1.3",
                    "distance": 17946
                },
                {
                    "node": "2.1.4",
                    "distance": 17946
                },
                {
                    "node": "2.2.1",
                    "distance": 17946
                },
                {
                    "node": "2.2.2",
                    "distance": 17946
                },
                {
                    "node": "2.2.3",
                    "distance": 17946
                },
                {
                    "node": "2.2.4",
                    "distance": 17946
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 27257
                },
                {
                    "node": "2.6.2",
                    "distance": 27257
                },
                {
                    "node": "2.6.3",
                    "distance": 27257
                },
                {
                    "node": "2.6.4",
                    "distance": 27257
                },
                {
                    "node": "2.7.1",
                    "distance": 33670
                },
                {
                    "node": "2.7.2",
                    "distance": 33670
                },
                {
                    "node": "2.7.3",
                    "distance": 33670
                },
                {
                    "node": "2.7.4",
                    "distance": 33670
                }
            ]
        },
        {
            "2.2": [
                {
                    "node": "1.1.1",
                    "distance": 18522
                },
                {
                    "node": "1.1.2",
                    "distance": 18522
                },
                {
                    "node": "1.1.3",
                    "distance": 18522
                },
                {
                    "node": "1.1.4",
                    "distance": 18522
                },
                {
                    "node": "1.2.1",
                    "distance": 18522
                },
                {
                    "node": "1.2.2",
                    "distance": 18522
                },
                {
                    "node": "1.2.3",
                    "distance": 18522
                },
                {
                    "node": "1.2.4",
                    "distance": 18522
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 27257
                },
                {
                    "node": "1.6.2",
                    "distance": 27257
                },
                {
                    "node": "1.6.3",
                    "distance": 27257
                },
                {
                    "node": "1.6.4",
                    "distance": 27257
                },
                {
                    "node": "1.7.1",
                    "distance": 33670
                },
                {
                    "node": "1.7.2",
                    "distance": 33670
                },
                {
                    "node": "1.7.3",
                    "distance": 33670
                },
                {
                    "node": "1.7.4",
                    "distance": 33670
                },
                {
                    "node": "2.1.1",
                    "distance": 17946
                },
                {
                    "node": "2.1.2",
                    "distance": 17946
                },
                {
                    "node": "2.1.3",
                    "distance": 17946
                },
                {
                    "node": "2.1.4",
                    "distance": 17946
                },
                {
                    "node": "2.2.1",
                    "distance": 17946
                },
                {
                    "node": "2.2.2",
                    "distance": 17946
                },
                {
                    "node": "2.2.3",
                    "distance": 17946
                },
                {
                    "node": "2.2.4",
                    "distance": 17946
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 27257
                },
                {
                    "node": "2.6.2",
                    "distance": 27257
                },
                {
                    "node": "2.6.3",
                    "distance": 27257
                },
                {
                    "node": "2.6.4",
                    "distance": 27257
                },
                {
                    "node": "2.7.1",
                    "distance": 33670
                },
                {
                    "node": "2.7.2",
                    "distance": 33670
                },
                {
                    "node": "2.7.3",
                    "distance": 33670
                },
                {
                    "node": "2.7.4",
                    "distance": 33670
                }
            ]
        },
        {
            "2.3": [
                {
                    "node": "1.1.1",
                    "distance": 18522
                },
                {
                    "node": "1.1.2",
                    "distance": 18522
                },
                {
                    "node": "1.1.3",
                    "distance": 18522
                },
                {
                    "node": "1.1.4",
                    "distance": 18522
                },
                {
                    "node": "1.2.1",
                    "distance": 18522
                },
                {
                    "node": "1.2.2",
                    "distance": 18522
                },
                {
                    "node": "1.2.3",
                    "distance": 18522
                },
                {
                    "node": "1.2.4",
                    "distance": 18522
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 27257
                },
                {
                    "node": "1.6.2",
                    "distance": 27257
                },
                {
                    "node": "1.6.3",
                    "distance": 27257
                },
                {
                    "node": "1.6.4",
                    "distance": 27257
                },
                {
                    "node": "1.7.1",
                    "distance": 33670
                },
                {
                    "node": "1.7.2",
                    "distance": 33670
                },
                {
                    "node": "1.7.3",
                    "distance": 33670
                },
                {
                    "node": "1.7.4",
                    "distance": 33670
                },
                {
                    "node": "2.1.1",
                    "distance": 17946
                },
                {
                    "node": "2.1.2",
                    "distance": 17946
                },
                {
                    "node": "2.1.3",
                    "distance": 17946
                },
                {
                    "node": "2.1.4",
                    "distance": 17946
                },
                {
                    "node": "2.2.1",
                    "distance": 17946
                },
                {
                    "node": "2.2.2",
                    "distance": 17946
                },
                {
                    "node": "2.2.3",
                    "distance": 17946
                },
                {
                    "node": "2.2.4",
                    "distance": 17946
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 27257
                },
                {
                    "node": "2.6.2",
                    "distance": 27257
                },
                {
                    "node": "2.6.3",
                    "distance": 27257
                },
                {
                    "node": "2.6.4",
                    "distance": 27257
                },
                {
                    "node": "2.7.1",
                    "distance": 33670
                },
                {
                    "node": "2.7.2",
                    "distance": 33670
                },
                {
                    "node": "2.7.3",
                    "distance": 33670
                },
                {
                    "node": "2.7.4",
                    "distance": 33670
                }
            ]
        },
        {
            "2.4": [
                {
                    "node": "1.1.1",
                    "distance": 18522
                },
                {
                    "node": "1.1.2",
                    "distance": 18522
                },
                {
                    "node": "1.1.3",
                    "distance": 18522
                },
                {
                    "node": "1.1.4",
                    "distance": 18522
                },
                {
                    "node": "1.2.1",
                    "distance": 18522
                },
                {
                    "node": "1.2.2",
                    "distance": 18522
                },
                {
                    "node": "1.2.3",
                    "distance": 18522
                },
                {
                    "node": "1.2.4",
                    "distance": 18522
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 27257
                },
                {
                    "node": "1.6.2",
                    "distance": 27257
                },
                {
                    "node": "1.6.3",
                    "distance": 27257
                },
                {
                    "node": "1.6.4",
                    "distance": 27257
                },
                {
                    "node": "1.7.1",
                    "distance": 33670
                },
                {
                    "node": "1.7.2",
                    "distance": 33670
                },
                {
                    "node": "1.7.3",
                    "distance": 33670
                },
                {
                    "node": "1.7.4",
                    "distance": 33670
                },
                {
                    "node": "2.1.1",
                    "distance": 17946
                },
                {
                    "node": "2.1.2",
                    "distance": 17946
                },
                {
                    "node": "2.1.3",
                    "distance": 17946
                },
                {
                    "node": "2.1.4",
                    "distance": 17946
                },
                {
                    "node": "2.2.1",
                    "distance": 17946
                },
                {
                    "node": "2.2.2",
                    "distance": 17946
                },
                {
                    "node": "2.2.3",
                    "distance": 17946
                },
                {
                    "node": "2.2.4",
                    "distance": 17946
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 27257
                },
                {
                    "node": "2.6.2",
                    "distance": 27257
                },
                {
                    "node": "2.6.3",
                    "distance": 27257
                },
                {
                    "node": "2.6.4",
                    "distance": 27257
                },
                {
                    "node": "2.7.1",
                    "distance": 33670
                },
                {
                    "node": "2.7.2",
                    "distance": 33670
                },
                {
                    "node": "2.7.3",
                    "distance": 33670
                },
                {
                    "node": "2.7.4",
                    "distance": 33670
                }
            ]
        },
        {
            "2.5": [
                {
                    "node": "1.1.1",
                    "distance": 22876
                },
                {
                    "node": "1.1.2",
                    "distance": 22876
                },
                {
                    "node": "1.1.3",
                    "distance": 22876
                },
                {
                    "node": "1.1.4",
                    "distance": 22876
                },
                {
                    "node": "1.2.1",
                    "distance": 19704
                },
                {
                    "node": "1.2.2",
                    "distance": 19704
                },
                {
                    "node": "1.2.3",
                    "distance": 19704
                },
                {
                    "node": "1.2.4",
                    "distance": 19704
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 22588
                },
                {
                    "node": "2.1.2",
                    "distance": 22588
                },
                {
                    "node": "2.1.3",
                    "distance": 22588
                },
                {
                    "node": "2.1.4",
                    "distance": 22588
                },
                {
                    "node": "2.2.1",
                    "distance": 19416
                },
                {
                    "node": "2.2.2",
                    "distance": 19416
                },
                {
                    "node": "2.2.3",
                    "distance": 19416
                },
                {
                    "node": "2.2.4",
                    "distance": 19416
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "2.6": [
                {
                    "node": "1.1.1",
                    "distance": 22876
                },
                {
                    "node": "1.1.2",
                    "distance": 22876
                },
                {
                    "node": "1.1.3",
                    "distance": 22876
                },
                {
                    "node": "1.1.4",
                    "distance": 22876
                },
                {
                    "node": "1.2.1",
                    "distance": 19704
                },
                {
                    "node": "1.2.2",
                    "distance": 19704
                },
                {
                    "node": "1.2.3",
                    "distance": 19704
                },
                {
                    "node": "1.2.4",
                    "distance": 19704
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 22588
                },
                {
                    "node": "2.1.2",
                    "distance": 22588
                },
                {
                    "node": "2.1.3",
                    "distance": 22588
                },
                {
                    "node": "2.1.4",
                    "distance": 22588
                },
                {
                    "node": "2.2.1",
                    "distance": 19416
                },
                {
                    "node": "2.2.2",
                    "distance": 19416
                },
                {
                    "node": "2.2.3",
                    "distance": 19416
                },
                {
                    "node": "2.2.4",
                    "distance": 19416
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "3.1": [
                {
                    "node": "1.1.1",
                    "distance": 22876
                },
                {
                    "node": "1.1.2",
                    "distance": 22876
                },
                {
                    "node": "1.1.3",
                    "distance": 22876
                },
                {
                    "node": "1.1.4",
                    "distance": 22876
                },
                {
                    "node": "1.2.1",
                    "distance": 19704
                },
                {
                    "node": "1.2.2",
                    "distance": 19704
                },
                {
                    "node": "1.2.3",
                    "distance": 19704
                },
                {
                    "node": "1.2.4",
                    "distance": 19704
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 22588
                },
                {
                    "node": "2.1.2",
                    "distance": 22588
                },
                {
                    "node": "2.1.3",
                    "distance": 22588
                },
                {
                    "node": "2.1.4",
                    "distance": 22588
                },
                {
                    "node": "2.2.1",
                    "distance": 19416
                },
                {
                    "node": "2.2.2",
                    "distance": 19416
                },
                {
                    "node": "2.2.3",
                    "distance": 19416
                },
                {
                    "node": "2.2.4",
                    "distance": 19416
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "3.2": [
                {
                    "node": "1.1.1",
                    "distance": 22876
                },
                {
                    "node": "1.1.2",
                    "distance": 22876
                },
                {
                    "node": "1.1.3",
                    "distance": 22876
                },
                {
                    "node": "1.1.4",
                    "distance": 22876
                },
                {
                    "node": "1.2.1",
                    "distance": 19704
                },
                {
                    "node": "1.2.2",
                    "distance": 19704
                },
                {
                    "node": "1.2.3",
                    "distance": 19704
                },
                {
                    "node": "1.2.4",
                    "distance": 19704
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 22588
                },
                {
                    "node": "2.1.2",
                    "distance": 22588
                },
                {
                    "node": "2.1.3",
                    "distance": 22588
                },
                {
                    "node": "2.1.4",
                    "distance": 22588
                },
                {
                    "node": "2.2.1",
                    "distance": 19416
                },
                {
                    "node": "2.2.2",
                    "distance": 19416
                },
                {
                    "node": "2.2.3",
                    "distance": 19416
                },
                {
                    "node": "2.2.4",
                    "distance": 19416
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "3.3": [
                {
                    "node": "1.1.1",
                    "distance": 22876
                },
                {
                    "node": "1.1.2",
                    "distance": 22876
                },
                {
                    "node": "1.1.3",
                    "distance": 22876
                },
                {
                    "node": "1.1.4",
                    "distance": 22876
                },
                {
                    "node": "1.2.1",
                    "distance": 19704
                },
                {
                    "node": "1.2.2",
                    "distance": 19704
                },
                {
                    "node": "1.2.3",
                    "distance": 19704
                },
                {
                    "node": "1.2.4",
                    "distance": 19704
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 22588
                },
                {
                    "node": "2.1.2",
                    "distance": 22588
                },
                {
                    "node": "2.1.3",
                    "distance": 22588
                },
                {
                    "node": "2.1.4",
                    "distance": 22588
                },
                {
                    "node": "2.2.1",
                    "distance": 19416
                },
                {
                    "node": "2.2.2",
                    "distance": 19416
                },
                {
                    "node": "2.2.3",
                    "distance": 19416
                },
                {
                    "node": "2.2.4",
                    "distance": 19416
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "3.4": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "3.5": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "3.6": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "4.1": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "4.2": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "4.3": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "4.4": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "4.5": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "4.6": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        }
    ],
    "2.1": [
        {
            "1.1": [
                {
                    "node": "1.1.1",
                    "distance": 18522
                },
                {
                    "node": "1.1.2",
                    "distance": 18522
                },
                {
                    "node": "1.1.3",
                    "distance": 18522
                },
                {
                    "node": "1.1.4",
                    "distance": 18522
                },
                {
                    "node": "1.2.1",
                    "distance": 18522
                },
                {
                    "node": "1.2.2",
                    "distance": 18522
                },
                {
                    "node": "1.2.3",
                    "distance": 18522
                },
                {
                    "node": "1.2.4",
                    "distance": 18522
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 27257
                },
                {
                    "node": "1.6.2",
                    "distance": 27257
                },
                {
                    "node": "1.6.3",
                    "distance": 27257
                },
                {
                    "node": "1.6.4",
                    "distance": 27257
                },
                {
                    "node": "1.7.1",
                    "distance": 33670
                },
                {
                    "node": "1.7.2",
                    "distance": 33670
                },
                {
                    "node": "1.7.3",
                    "distance": 33670
                },
                {
                    "node": "1.7.4",
                    "distance": 33670
                },
                {
                    "node": "2.1.1",
                    "distance": 17946
                },
                {
                    "node": "2.1.2",
                    "distance": 17946
                },
                {
                    "node": "2.1.3",
                    "distance": 17946
                },
                {
                    "node": "2.1.4",
                    "distance": 17946
                },
                {
                    "node": "2.2.1",
                    "distance": 17946
                },
                {
                    "node": "2.2.2",
                    "distance": 17946
                },
                {
                    "node": "2.2.3",
                    "distance": 17946
                },
                {
                    "node": "2.2.4",
                    "distance": 17946
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 27257
                },
                {
                    "node": "2.6.2",
                    "distance": 27257
                },
                {
                    "node": "2.6.3",
                    "distance": 27257
                },
                {
                    "node": "2.6.4",
                    "distance": 27257
                },
                {
                    "node": "2.7.1",
                    "distance": 33670
                },
                {
                    "node": "2.7.2",
                    "distance": 33670
                },
                {
                    "node": "2.7.3",
                    "distance": 33670
                },
                {
                    "node": "2.7.4",
                    "distance": 33670
                }
            ]
        },
        {
            "1.2": [
                {
                    "node": "1.1.1",
                    "distance": 18522
                },
                {
                    "node": "1.1.2",
                    "distance": 18522
                },
                {
                    "node": "1.1.3",
                    "distance": 18522
                },
                {
                    "node": "1.1.4",
                    "distance": 18522
                },
                {
                    "node": "1.2.1",
                    "distance": 18522
                },
                {
                    "node": "1.2.2",
                    "distance": 18522
                },
                {
                    "node": "1.2.3",
                    "distance": 18522
                },
                {
                    "node": "1.2.4",
                    "distance": 18522
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 27257
                },
                {
                    "node": "1.6.2",
                    "distance": 27257
                },
                {
                    "node": "1.6.3",
                    "distance": 27257
                },
                {
                    "node": "1.6.4",
                    "distance": 27257
                },
                {
                    "node": "1.7.1",
                    "distance": 33670
                },
                {
                    "node": "1.7.2",
                    "distance": 33670
                },
                {
                    "node": "1.7.3",
                    "distance": 33670
                },
                {
                    "node": "1.7.4",
                    "distance": 33670
                },
                {
                    "node": "2.1.1",
                    "distance": 17946
                },
                {
                    "node": "2.1.2",
                    "distance": 17946
                },
                {
                    "node": "2.1.3",
                    "distance": 17946
                },
                {
                    "node": "2.1.4",
                    "distance": 17946
                },
                {
                    "node": "2.2.1",
                    "distance": 17946
                },
                {
                    "node": "2.2.2",
                    "distance": 17946
                },
                {
                    "node": "2.2.3",
                    "distance": 17946
                },
                {
                    "node": "2.2.4",
                    "distance": 17946
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 27257
                },
                {
                    "node": "2.6.2",
                    "distance": 27257
                },
                {
                    "node": "2.6.3",
                    "distance": 27257
                },
                {
                    "node": "2.6.4",
                    "distance": 27257
                },
                {
                    "node": "2.7.1",
                    "distance": 33670
                },
                {
                    "node": "2.7.2",
                    "distance": 33670
                },
                {
                    "node": "2.7.3",
                    "distance": 33670
                },
                {
                    "node": "2.7.4",
                    "distance": 33670
                }
            ]
        },
        {
            "1.3": [
                {
                    "node": "1.1.1",
                    "distance": 18522
                },
                {
                    "node": "1.1.2",
                    "distance": 18522
                },
                {
                    "node": "1.1.3",
                    "distance": 18522
                },
                {
                    "node": "1.1.4",
                    "distance": 18522
                },
                {
                    "node": "1.2.1",
                    "distance": 18522
                },
                {
                    "node": "1.2.2",
                    "distance": 18522
                },
                {
                    "node": "1.2.3",
                    "distance": 18522
                },
                {
                    "node": "1.2.4",
                    "distance": 18522
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 27257
                },
                {
                    "node": "1.6.2",
                    "distance": 27257
                },
                {
                    "node": "1.6.3",
                    "distance": 27257
                },
                {
                    "node": "1.6.4",
                    "distance": 27257
                },
                {
                    "node": "1.7.1",
                    "distance": 33670
                },
                {
                    "node": "1.7.2",
                    "distance": 33670
                },
                {
                    "node": "1.7.3",
                    "distance": 33670
                },
                {
                    "node": "1.7.4",
                    "distance": 33670
                },
                {
                    "node": "2.1.1",
                    "distance": 17946
                },
                {
                    "node": "2.1.2",
                    "distance": 17946
                },
                {
                    "node": "2.1.3",
                    "distance": 17946
                },
                {
                    "node": "2.1.4",
                    "distance": 17946
                },
                {
                    "node": "2.2.1",
                    "distance": 17946
                },
                {
                    "node": "2.2.2",
                    "distance": 17946
                },
                {
                    "node": "2.2.3",
                    "distance": 17946
                },
                {
                    "node": "2.2.4",
                    "distance": 17946
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 27257
                },
                {
                    "node": "2.6.2",
                    "distance": 27257
                },
                {
                    "node": "2.6.3",
                    "distance": 27257
                },
                {
                    "node": "2.6.4",
                    "distance": 27257
                },
                {
                    "node": "2.7.1",
                    "distance": 33670
                },
                {
                    "node": "2.7.2",
                    "distance": 33670
                },
                {
                    "node": "2.7.3",
                    "distance": 33670
                },
                {
                    "node": "2.7.4",
                    "distance": 33670
                }
            ]
        },
        {
            "1.4": [
                {
                    "node": "1.1.1",
                    "distance": 18522
                },
                {
                    "node": "1.1.2",
                    "distance": 18522
                },
                {
                    "node": "1.1.3",
                    "distance": 18522
                },
                {
                    "node": "1.1.4",
                    "distance": 18522
                },
                {
                    "node": "1.2.1",
                    "distance": 18522
                },
                {
                    "node": "1.2.2",
                    "distance": 18522
                },
                {
                    "node": "1.2.3",
                    "distance": 18522
                },
                {
                    "node": "1.2.4",
                    "distance": 18522
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 27257
                },
                {
                    "node": "1.6.2",
                    "distance": 27257
                },
                {
                    "node": "1.6.3",
                    "distance": 27257
                },
                {
                    "node": "1.6.4",
                    "distance": 27257
                },
                {
                    "node": "1.7.1",
                    "distance": 33670
                },
                {
                    "node": "1.7.2",
                    "distance": 33670
                },
                {
                    "node": "1.7.3",
                    "distance": 33670
                },
                {
                    "node": "1.7.4",
                    "distance": 33670
                },
                {
                    "node": "2.1.1",
                    "distance": 17946
                },
                {
                    "node": "2.1.2",
                    "distance": 17946
                },
                {
                    "node": "2.1.3",
                    "distance": 17946
                },
                {
                    "node": "2.1.4",
                    "distance": 17946
                },
                {
                    "node": "2.2.1",
                    "distance": 17946
                },
                {
                    "node": "2.2.2",
                    "distance": 17946
                },
                {
                    "node": "2.2.3",
                    "distance": 17946
                },
                {
                    "node": "2.2.4",
                    "distance": 17946
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 27257
                },
                {
                    "node": "2.6.2",
                    "distance": 27257
                },
                {
                    "node": "2.6.3",
                    "distance": 27257
                },
                {
                    "node": "2.6.4",
                    "distance": 27257
                },
                {
                    "node": "2.7.1",
                    "distance": 33670
                },
                {
                    "node": "2.7.2",
                    "distance": 33670
                },
                {
                    "node": "2.7.3",
                    "distance": 33670
                },
                {
                    "node": "2.7.4",
                    "distance": 33670
                }
            ]
        },
        {
            "1.5": [
                {
                    "node": "1.1.1",
                    "distance": 18522
                },
                {
                    "node": "1.1.2",
                    "distance": 18522
                },
                {
                    "node": "1.1.3",
                    "distance": 18522
                },
                {
                    "node": "1.1.4",
                    "distance": 18522
                },
                {
                    "node": "1.2.1",
                    "distance": 18522
                },
                {
                    "node": "1.2.2",
                    "distance": 18522
                },
                {
                    "node": "1.2.3",
                    "distance": 18522
                },
                {
                    "node": "1.2.4",
                    "distance": 18522
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 27257
                },
                {
                    "node": "1.6.2",
                    "distance": 27257
                },
                {
                    "node": "1.6.3",
                    "distance": 27257
                },
                {
                    "node": "1.6.4",
                    "distance": 27257
                },
                {
                    "node": "1.7.1",
                    "distance": 33670
                },
                {
                    "node": "1.7.2",
                    "distance": 33670
                },
                {
                    "node": "1.7.3",
                    "distance": 33670
                },
                {
                    "node": "1.7.4",
                    "distance": 33670
                },
                {
                    "node": "2.1.1",
                    "distance": 17946
                },
                {
                    "node": "2.1.2",
                    "distance": 17946
                },
                {
                    "node": "2.1.3",
                    "distance": 17946
                },
                {
                    "node": "2.1.4",
                    "distance": 17946
                },
                {
                    "node": "2.2.1",
                    "distance": 17946
                },
                {
                    "node": "2.2.2",
                    "distance": 17946
                },
                {
                    "node": "2.2.3",
                    "distance": 17946
                },
                {
                    "node": "2.2.4",
                    "distance": 17946
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 27257
                },
                {
                    "node": "2.6.2",
                    "distance": 27257
                },
                {
                    "node": "2.6.3",
                    "distance": 27257
                },
                {
                    "node": "2.6.4",
                    "distance": 27257
                },
                {
                    "node": "2.7.1",
                    "distance": 33670
                },
                {
                    "node": "2.7.2",
                    "distance": 33670
                },
                {
                    "node": "2.7.3",
                    "distance": 33670
                },
                {
                    "node": "2.7.4",
                    "distance": 33670
                }
            ]
        },
        {
            "1.6": [
                {
                    "node": "1.1.1",
                    "distance": 18522
                },
                {
                    "node": "1.1.2",
                    "distance": 18522
                },
                {
                    "node": "1.1.3",
                    "distance": 18522
                },
                {
                    "node": "1.1.4",
                    "distance": 18522
                },
                {
                    "node": "1.2.1",
                    "distance": 18522
                },
                {
                    "node": "1.2.2",
                    "distance": 18522
                },
                {
                    "node": "1.2.3",
                    "distance": 18522
                },
                {
                    "node": "1.2.4",
                    "distance": 18522
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 27257
                },
                {
                    "node": "1.6.2",
                    "distance": 27257
                },
                {
                    "node": "1.6.3",
                    "distance": 27257
                },
                {
                    "node": "1.6.4",
                    "distance": 27257
                },
                {
                    "node": "1.7.1",
                    "distance": 33670
                },
                {
                    "node": "1.7.2",
                    "distance": 33670
                },
                {
                    "node": "1.7.3",
                    "distance": 33670
                },
                {
                    "node": "1.7.4",
                    "distance": 33670
                },
                {
                    "node": "2.1.1",
                    "distance": 17946
                },
                {
                    "node": "2.1.2",
                    "distance": 17946
                },
                {
                    "node": "2.1.3",
                    "distance": 17946
                },
                {
                    "node": "2.1.4",
                    "distance": 17946
                },
                {
                    "node": "2.2.1",
                    "distance": 17946
                },
                {
                    "node": "2.2.2",
                    "distance": 17946
                },
                {
                    "node": "2.2.3",
                    "distance": 17946
                },
                {
                    "node": "2.2.4",
                    "distance": 17946
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 27257
                },
                {
                    "node": "2.6.2",
                    "distance": 27257
                },
                {
                    "node": "2.6.3",
                    "distance": 27257
                },
                {
                    "node": "2.6.4",
                    "distance": 27257
                },
                {
                    "node": "2.7.1",
                    "distance": 33670
                },
                {
                    "node": "2.7.2",
                    "distance": 33670
                },
                {
                    "node": "2.7.3",
                    "distance": 33670
                },
                {
                    "node": "2.7.4",
                    "distance": 33670
                }
            ]
        },
        {
            "2.1": [
                {
                    "node": "1.1.1",
                    "distance": 18522
                },
                {
                    "node": "1.1.2",
                    "distance": 18522
                },
                {
                    "node": "1.1.3",
                    "distance": 18522
                },
                {
                    "node": "1.1.4",
                    "distance": 18522
                },
                {
                    "node": "1.2.1",
                    "distance": 18522
                },
                {
                    "node": "1.2.2",
                    "distance": 18522
                },
                {
                    "node": "1.2.3",
                    "distance": 18522
                },
                {
                    "node": "1.2.4",
                    "distance": 18522
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 18522
                },
                {
                    "node": "1.4.2",
                    "distance": 18522
                },
                {
                    "node": "1.4.3",
                    "distance": 18522
                },
                {
                    "node": "1.4.4",
                    "distance": 18522
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 20886
                },
                {
                    "node": "1.6.2",
                    "distance": 20886
                },
                {
                    "node": "1.6.3",
                    "distance": 20886
                },
                {
                    "node": "1.6.4",
                    "distance": 20886
                },
                {
                    "node": "1.7.1",
                    "distance": 27230
                },
                {
                    "node": "1.7.2",
                    "distance": 27230
                },
                {
                    "node": "1.7.3",
                    "distance": 27230
                },
                {
                    "node": "1.7.4",
                    "distance": 27230
                },
                {
                    "node": "2.1.1",
                    "distance": 17946
                },
                {
                    "node": "2.1.2",
                    "distance": 17946
                },
                {
                    "node": "2.1.3",
                    "distance": 17946
                },
                {
                    "node": "2.1.4",
                    "distance": 17946
                },
                {
                    "node": "2.2.1",
                    "distance": 17946
                },
                {
                    "node": "2.2.2",
                    "distance": 17946
                },
                {
                    "node": "2.2.3",
                    "distance": 17946
                },
                {
                    "node": "2.2.4",
                    "distance": 17946
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 17946
                },
                {
                    "node": "2.4.2",
                    "distance": 17946
                },
                {
                    "node": "2.4.3",
                    "distance": 17946
                },
                {
                    "node": "2.4.4",
                    "distance": 17946
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 20886
                },
                {
                    "node": "2.6.2",
                    "distance": 20886
                },
                {
                    "node": "2.6.3",
                    "distance": 20886
                },
                {
                    "node": "2.6.4",
                    "distance": 20886
                },
                {
                    "node": "2.7.1",
                    "distance": 27230
                },
                {
                    "node": "2.7.2",
                    "distance": 27230
                },
                {
                    "node": "2.7.3",
                    "distance": 27230
                },
                {
                    "node": "2.7.4",
                    "distance": 27230
                }
            ]
        },
        {
            "2.2": [
                {
                    "node": "1.1.1",
                    "distance": 18522
                },
                {
                    "node": "1.1.2",
                    "distance": 18522
                },
                {
                    "node": "1.1.3",
                    "distance": 18522
                },
                {
                    "node": "1.1.4",
                    "distance": 18522
                },
                {
                    "node": "1.2.1",
                    "distance": 18522
                },
                {
                    "node": "1.2.2",
                    "distance": 18522
                },
                {
                    "node": "1.2.3",
                    "distance": 18522
                },
                {
                    "node": "1.2.4",
                    "distance": 18522
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 18522
                },
                {
                    "node": "1.4.2",
                    "distance": 18522
                },
                {
                    "node": "1.4.3",
                    "distance": 18522
                },
                {
                    "node": "1.4.4",
                    "distance": 18522
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 20886
                },
                {
                    "node": "1.6.2",
                    "distance": 20886
                },
                {
                    "node": "1.6.3",
                    "distance": 20886
                },
                {
                    "node": "1.6.4",
                    "distance": 20886
                },
                {
                    "node": "1.7.1",
                    "distance": 27230
                },
                {
                    "node": "1.7.2",
                    "distance": 27230
                },
                {
                    "node": "1.7.3",
                    "distance": 27230
                },
                {
                    "node": "1.7.4",
                    "distance": 27230
                },
                {
                    "node": "2.1.1",
                    "distance": 17946
                },
                {
                    "node": "2.1.2",
                    "distance": 17946
                },
                {
                    "node": "2.1.3",
                    "distance": 17946
                },
                {
                    "node": "2.1.4",
                    "distance": 17946
                },
                {
                    "node": "2.2.1",
                    "distance": 17946
                },
                {
                    "node": "2.2.2",
                    "distance": 17946
                },
                {
                    "node": "2.2.3",
                    "distance": 17946
                },
                {
                    "node": "2.2.4",
                    "distance": 17946
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 17946
                },
                {
                    "node": "2.4.2",
                    "distance": 17946
                },
                {
                    "node": "2.4.3",
                    "distance": 17946
                },
                {
                    "node": "2.4.4",
                    "distance": 17946
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 20886
                },
                {
                    "node": "2.6.2",
                    "distance": 20886
                },
                {
                    "node": "2.6.3",
                    "distance": 20886
                },
                {
                    "node": "2.6.4",
                    "distance": 20886
                },
                {
                    "node": "2.7.1",
                    "distance": 27230
                },
                {
                    "node": "2.7.2",
                    "distance": 27230
                },
                {
                    "node": "2.7.3",
                    "distance": 27230
                },
                {
                    "node": "2.7.4",
                    "distance": 27230
                }
            ]
        },
        {
            "2.3": [
                {
                    "node": "1.1.1",
                    "distance": 18522
                },
                {
                    "node": "1.1.2",
                    "distance": 18522
                },
                {
                    "node": "1.1.3",
                    "distance": 18522
                },
                {
                    "node": "1.1.4",
                    "distance": 18522
                },
                {
                    "node": "1.2.1",
                    "distance": 18522
                },
                {
                    "node": "1.2.2",
                    "distance": 18522
                },
                {
                    "node": "1.2.3",
                    "distance": 18522
                },
                {
                    "node": "1.2.4",
                    "distance": 18522
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 18522
                },
                {
                    "node": "1.4.2",
                    "distance": 18522
                },
                {
                    "node": "1.4.3",
                    "distance": 18522
                },
                {
                    "node": "1.4.4",
                    "distance": 18522
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 20886
                },
                {
                    "node": "1.6.2",
                    "distance": 20886
                },
                {
                    "node": "1.6.3",
                    "distance": 20886
                },
                {
                    "node": "1.6.4",
                    "distance": 20886
                },
                {
                    "node": "1.7.1",
                    "distance": 27230
                },
                {
                    "node": "1.7.2",
                    "distance": 27230
                },
                {
                    "node": "1.7.3",
                    "distance": 27230
                },
                {
                    "node": "1.7.4",
                    "distance": 27230
                },
                {
                    "node": "2.1.1",
                    "distance": 17946
                },
                {
                    "node": "2.1.2",
                    "distance": 17946
                },
                {
                    "node": "2.1.3",
                    "distance": 17946
                },
                {
                    "node": "2.1.4",
                    "distance": 17946
                },
                {
                    "node": "2.2.1",
                    "distance": 17946
                },
                {
                    "node": "2.2.2",
                    "distance": 17946
                },
                {
                    "node": "2.2.3",
                    "distance": 17946
                },
                {
                    "node": "2.2.4",
                    "distance": 17946
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 17946
                },
                {
                    "node": "2.4.2",
                    "distance": 17946
                },
                {
                    "node": "2.4.3",
                    "distance": 17946
                },
                {
                    "node": "2.4.4",
                    "distance": 17946
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 20886
                },
                {
                    "node": "2.6.2",
                    "distance": 20886
                },
                {
                    "node": "2.6.3",
                    "distance": 20886
                },
                {
                    "node": "2.6.4",
                    "distance": 20886
                },
                {
                    "node": "2.7.1",
                    "distance": 27230
                },
                {
                    "node": "2.7.2",
                    "distance": 27230
                },
                {
                    "node": "2.7.3",
                    "distance": 27230
                },
                {
                    "node": "2.7.4",
                    "distance": 27230
                }
            ]
        },
        {
            "2.4": [
                {
                    "node": "1.1.1",
                    "distance": 18522
                },
                {
                    "node": "1.1.2",
                    "distance": 18522
                },
                {
                    "node": "1.1.3",
                    "distance": 18522
                },
                {
                    "node": "1.1.4",
                    "distance": 18522
                },
                {
                    "node": "1.2.1",
                    "distance": 18522
                },
                {
                    "node": "1.2.2",
                    "distance": 18522
                },
                {
                    "node": "1.2.3",
                    "distance": 18522
                },
                {
                    "node": "1.2.4",
                    "distance": 18522
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 18522
                },
                {
                    "node": "1.4.2",
                    "distance": 18522
                },
                {
                    "node": "1.4.3",
                    "distance": 18522
                },
                {
                    "node": "1.4.4",
                    "distance": 18522
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 20886
                },
                {
                    "node": "1.6.2",
                    "distance": 20886
                },
                {
                    "node": "1.6.3",
                    "distance": 20886
                },
                {
                    "node": "1.6.4",
                    "distance": 20886
                },
                {
                    "node": "1.7.1",
                    "distance": 27230
                },
                {
                    "node": "1.7.2",
                    "distance": 27230
                },
                {
                    "node": "1.7.3",
                    "distance": 27230
                },
                {
                    "node": "1.7.4",
                    "distance": 27230
                },
                {
                    "node": "2.1.1",
                    "distance": 17946
                },
                {
                    "node": "2.1.2",
                    "distance": 17946
                },
                {
                    "node": "2.1.3",
                    "distance": 17946
                },
                {
                    "node": "2.1.4",
                    "distance": 17946
                },
                {
                    "node": "2.2.1",
                    "distance": 17946
                },
                {
                    "node": "2.2.2",
                    "distance": 17946
                },
                {
                    "node": "2.2.3",
                    "distance": 17946
                },
                {
                    "node": "2.2.4",
                    "distance": 17946
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 17946
                },
                {
                    "node": "2.4.2",
                    "distance": 17946
                },
                {
                    "node": "2.4.3",
                    "distance": 17946
                },
                {
                    "node": "2.4.4",
                    "distance": 17946
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 20886
                },
                {
                    "node": "2.6.2",
                    "distance": 20886
                },
                {
                    "node": "2.6.3",
                    "distance": 20886
                },
                {
                    "node": "2.6.4",
                    "distance": 20886
                },
                {
                    "node": "2.7.1",
                    "distance": 27230
                },
                {
                    "node": "2.7.2",
                    "distance": 27230
                },
                {
                    "node": "2.7.3",
                    "distance": 27230
                },
                {
                    "node": "2.7.4",
                    "distance": 27230
                }
            ]
        },
        {
            "2.5": [
                {
                    "node": "1.1.1",
                    "distance": 22876
                },
                {
                    "node": "1.1.2",
                    "distance": 22876
                },
                {
                    "node": "1.1.3",
                    "distance": 22876
                },
                {
                    "node": "1.1.4",
                    "distance": 22876
                },
                {
                    "node": "1.2.1",
                    "distance": 19704
                },
                {
                    "node": "1.2.2",
                    "distance": 19704
                },
                {
                    "node": "1.2.3",
                    "distance": 19704
                },
                {
                    "node": "1.2.4",
                    "distance": 19704
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 18522
                },
                {
                    "node": "1.4.2",
                    "distance": 18522
                },
                {
                    "node": "1.4.3",
                    "distance": 18522
                },
                {
                    "node": "1.4.4",
                    "distance": 18522
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 19704
                },
                {
                    "node": "1.6.2",
                    "distance": 19704
                },
                {
                    "node": "1.6.3",
                    "distance": 19704
                },
                {
                    "node": "1.6.4",
                    "distance": 19704
                },
                {
                    "node": "1.7.1",
                    "distance": 22876
                },
                {
                    "node": "1.7.2",
                    "distance": 22876
                },
                {
                    "node": "1.7.3",
                    "distance": 22876
                },
                {
                    "node": "1.7.4",
                    "distance": 22876
                },
                {
                    "node": "2.1.1",
                    "distance": 22588
                },
                {
                    "node": "2.1.2",
                    "distance": 22588
                },
                {
                    "node": "2.1.3",
                    "distance": 22588
                },
                {
                    "node": "2.1.4",
                    "distance": 22588
                },
                {
                    "node": "2.2.1",
                    "distance": 19416
                },
                {
                    "node": "2.2.2",
                    "distance": 19416
                },
                {
                    "node": "2.2.3",
                    "distance": 19416
                },
                {
                    "node": "2.2.4",
                    "distance": 19416
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 17946
                },
                {
                    "node": "2.4.2",
                    "distance": 17946
                },
                {
                    "node": "2.4.3",
                    "distance": 17946
                },
                {
                    "node": "2.4.4",
                    "distance": 17946
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 19416
                },
                {
                    "node": "2.6.2",
                    "distance": 19416
                },
                {
                    "node": "2.6.3",
                    "distance": 19416
                },
                {
                    "node": "2.6.4",
                    "distance": 19416
                },
                {
                    "node": "2.7.1",
                    "distance": 22588
                },
                {
                    "node": "2.7.2",
                    "distance": 22588
                },
                {
                    "node": "2.7.3",
                    "distance": 22588
                },
                {
                    "node": "2.7.4",
                    "distance": 22588
                }
            ]
        },
        {
            "2.6": [
                {
                    "node": "1.1.1",
                    "distance": 22876
                },
                {
                    "node": "1.1.2",
                    "distance": 22876
                },
                {
                    "node": "1.1.3",
                    "distance": 22876
                },
                {
                    "node": "1.1.4",
                    "distance": 22876
                },
                {
                    "node": "1.2.1",
                    "distance": 19704
                },
                {
                    "node": "1.2.2",
                    "distance": 19704
                },
                {
                    "node": "1.2.3",
                    "distance": 19704
                },
                {
                    "node": "1.2.4",
                    "distance": 19704
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 18522
                },
                {
                    "node": "1.4.2",
                    "distance": 18522
                },
                {
                    "node": "1.4.3",
                    "distance": 18522
                },
                {
                    "node": "1.4.4",
                    "distance": 18522
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 19704
                },
                {
                    "node": "1.6.2",
                    "distance": 19704
                },
                {
                    "node": "1.6.3",
                    "distance": 19704
                },
                {
                    "node": "1.6.4",
                    "distance": 19704
                },
                {
                    "node": "1.7.1",
                    "distance": 22876
                },
                {
                    "node": "1.7.2",
                    "distance": 22876
                },
                {
                    "node": "1.7.3",
                    "distance": 22876
                },
                {
                    "node": "1.7.4",
                    "distance": 22876
                },
                {
                    "node": "2.1.1",
                    "distance": 22588
                },
                {
                    "node": "2.1.2",
                    "distance": 22588
                },
                {
                    "node": "2.1.3",
                    "distance": 22588
                },
                {
                    "node": "2.1.4",
                    "distance": 22588
                },
                {
                    "node": "2.2.1",
                    "distance": 19416
                },
                {
                    "node": "2.2.2",
                    "distance": 19416
                },
                {
                    "node": "2.2.3",
                    "distance": 19416
                },
                {
                    "node": "2.2.4",
                    "distance": 19416
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 17946
                },
                {
                    "node": "2.4.2",
                    "distance": 17946
                },
                {
                    "node": "2.4.3",
                    "distance": 17946
                },
                {
                    "node": "2.4.4",
                    "distance": 17946
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 19416
                },
                {
                    "node": "2.6.2",
                    "distance": 19416
                },
                {
                    "node": "2.6.3",
                    "distance": 19416
                },
                {
                    "node": "2.6.4",
                    "distance": 19416
                },
                {
                    "node": "2.7.1",
                    "distance": 22588
                },
                {
                    "node": "2.7.2",
                    "distance": 22588
                },
                {
                    "node": "2.7.3",
                    "distance": 22588
                },
                {
                    "node": "2.7.4",
                    "distance": 22588
                }
            ]
        },
        {
            "3.1": [
                {
                    "node": "1.1.1",
                    "distance": 22876
                },
                {
                    "node": "1.1.2",
                    "distance": 22876
                },
                {
                    "node": "1.1.3",
                    "distance": 22876
                },
                {
                    "node": "1.1.4",
                    "distance": 22876
                },
                {
                    "node": "1.2.1",
                    "distance": 19704
                },
                {
                    "node": "1.2.2",
                    "distance": 19704
                },
                {
                    "node": "1.2.3",
                    "distance": 19704
                },
                {
                    "node": "1.2.4",
                    "distance": 19704
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 18522
                },
                {
                    "node": "1.4.2",
                    "distance": 18522
                },
                {
                    "node": "1.4.3",
                    "distance": 18522
                },
                {
                    "node": "1.4.4",
                    "distance": 18522
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 19704
                },
                {
                    "node": "1.6.2",
                    "distance": 19704
                },
                {
                    "node": "1.6.3",
                    "distance": 19704
                },
                {
                    "node": "1.6.4",
                    "distance": 19704
                },
                {
                    "node": "1.7.1",
                    "distance": 22876
                },
                {
                    "node": "1.7.2",
                    "distance": 22876
                },
                {
                    "node": "1.7.3",
                    "distance": 22876
                },
                {
                    "node": "1.7.4",
                    "distance": 22876
                },
                {
                    "node": "2.1.1",
                    "distance": 22588
                },
                {
                    "node": "2.1.2",
                    "distance": 22588
                },
                {
                    "node": "2.1.3",
                    "distance": 22588
                },
                {
                    "node": "2.1.4",
                    "distance": 22588
                },
                {
                    "node": "2.2.1",
                    "distance": 19416
                },
                {
                    "node": "2.2.2",
                    "distance": 19416
                },
                {
                    "node": "2.2.3",
                    "distance": 19416
                },
                {
                    "node": "2.2.4",
                    "distance": 19416
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 17946
                },
                {
                    "node": "2.4.2",
                    "distance": 17946
                },
                {
                    "node": "2.4.3",
                    "distance": 17946
                },
                {
                    "node": "2.4.4",
                    "distance": 17946
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 19416
                },
                {
                    "node": "2.6.2",
                    "distance": 19416
                },
                {
                    "node": "2.6.3",
                    "distance": 19416
                },
                {
                    "node": "2.6.4",
                    "distance": 19416
                },
                {
                    "node": "2.7.1",
                    "distance": 22588
                },
                {
                    "node": "2.7.2",
                    "distance": 22588
                },
                {
                    "node": "2.7.3",
                    "distance": 22588
                },
                {
                    "node": "2.7.4",
                    "distance": 22588
                }
            ]
        },
        {
            "3.2": [
                {
                    "node": "1.1.1",
                    "distance": 22876
                },
                {
                    "node": "1.1.2",
                    "distance": 22876
                },
                {
                    "node": "1.1.3",
                    "distance": 22876
                },
                {
                    "node": "1.1.4",
                    "distance": 22876
                },
                {
                    "node": "1.2.1",
                    "distance": 19704
                },
                {
                    "node": "1.2.2",
                    "distance": 19704
                },
                {
                    "node": "1.2.3",
                    "distance": 19704
                },
                {
                    "node": "1.2.4",
                    "distance": 19704
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 18522
                },
                {
                    "node": "1.4.2",
                    "distance": 18522
                },
                {
                    "node": "1.4.3",
                    "distance": 18522
                },
                {
                    "node": "1.4.4",
                    "distance": 18522
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 19704
                },
                {
                    "node": "1.6.2",
                    "distance": 19704
                },
                {
                    "node": "1.6.3",
                    "distance": 19704
                },
                {
                    "node": "1.6.4",
                    "distance": 19704
                },
                {
                    "node": "1.7.1",
                    "distance": 22876
                },
                {
                    "node": "1.7.2",
                    "distance": 22876
                },
                {
                    "node": "1.7.3",
                    "distance": 22876
                },
                {
                    "node": "1.7.4",
                    "distance": 22876
                },
                {
                    "node": "2.1.1",
                    "distance": 22588
                },
                {
                    "node": "2.1.2",
                    "distance": 22588
                },
                {
                    "node": "2.1.3",
                    "distance": 22588
                },
                {
                    "node": "2.1.4",
                    "distance": 22588
                },
                {
                    "node": "2.2.1",
                    "distance": 19416
                },
                {
                    "node": "2.2.2",
                    "distance": 19416
                },
                {
                    "node": "2.2.3",
                    "distance": 19416
                },
                {
                    "node": "2.2.4",
                    "distance": 19416
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 17946
                },
                {
                    "node": "2.4.2",
                    "distance": 17946
                },
                {
                    "node": "2.4.3",
                    "distance": 17946
                },
                {
                    "node": "2.4.4",
                    "distance": 17946
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 19416
                },
                {
                    "node": "2.6.2",
                    "distance": 19416
                },
                {
                    "node": "2.6.3",
                    "distance": 19416
                },
                {
                    "node": "2.6.4",
                    "distance": 19416
                },
                {
                    "node": "2.7.1",
                    "distance": 22588
                },
                {
                    "node": "2.7.2",
                    "distance": 22588
                },
                {
                    "node": "2.7.3",
                    "distance": 22588
                },
                {
                    "node": "2.7.4",
                    "distance": 22588
                }
            ]
        },
        {
            "3.3": [
                {
                    "node": "1.1.1",
                    "distance": 22876
                },
                {
                    "node": "1.1.2",
                    "distance": 22876
                },
                {
                    "node": "1.1.3",
                    "distance": 22876
                },
                {
                    "node": "1.1.4",
                    "distance": 22876
                },
                {
                    "node": "1.2.1",
                    "distance": 19704
                },
                {
                    "node": "1.2.2",
                    "distance": 19704
                },
                {
                    "node": "1.2.3",
                    "distance": 19704
                },
                {
                    "node": "1.2.4",
                    "distance": 19704
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 18522
                },
                {
                    "node": "1.4.2",
                    "distance": 18522
                },
                {
                    "node": "1.4.3",
                    "distance": 18522
                },
                {
                    "node": "1.4.4",
                    "distance": 18522
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 19704
                },
                {
                    "node": "1.6.2",
                    "distance": 19704
                },
                {
                    "node": "1.6.3",
                    "distance": 19704
                },
                {
                    "node": "1.6.4",
                    "distance": 19704
                },
                {
                    "node": "1.7.1",
                    "distance": 22876
                },
                {
                    "node": "1.7.2",
                    "distance": 22876
                },
                {
                    "node": "1.7.3",
                    "distance": 22876
                },
                {
                    "node": "1.7.4",
                    "distance": 22876
                },
                {
                    "node": "2.1.1",
                    "distance": 22588
                },
                {
                    "node": "2.1.2",
                    "distance": 22588
                },
                {
                    "node": "2.1.3",
                    "distance": 22588
                },
                {
                    "node": "2.1.4",
                    "distance": 22588
                },
                {
                    "node": "2.2.1",
                    "distance": 19416
                },
                {
                    "node": "2.2.2",
                    "distance": 19416
                },
                {
                    "node": "2.2.3",
                    "distance": 19416
                },
                {
                    "node": "2.2.4",
                    "distance": 19416
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 17946
                },
                {
                    "node": "2.4.2",
                    "distance": 17946
                },
                {
                    "node": "2.4.3",
                    "distance": 17946
                },
                {
                    "node": "2.4.4",
                    "distance": 17946
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 19416
                },
                {
                    "node": "2.6.2",
                    "distance": 19416
                },
                {
                    "node": "2.6.3",
                    "distance": 19416
                },
                {
                    "node": "2.6.4",
                    "distance": 19416
                },
                {
                    "node": "2.7.1",
                    "distance": 22588
                },
                {
                    "node": "2.7.2",
                    "distance": 22588
                },
                {
                    "node": "2.7.3",
                    "distance": 22588
                },
                {
                    "node": "2.7.4",
                    "distance": 22588
                }
            ]
        },
        {
            "3.4": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 19704
                },
                {
                    "node": "1.6.2",
                    "distance": 19704
                },
                {
                    "node": "1.6.3",
                    "distance": 19704
                },
                {
                    "node": "1.6.4",
                    "distance": 19704
                },
                {
                    "node": "1.7.1",
                    "distance": 22876
                },
                {
                    "node": "1.7.2",
                    "distance": 22876
                },
                {
                    "node": "1.7.3",
                    "distance": 22876
                },
                {
                    "node": "1.7.4",
                    "distance": 22876
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 19416
                },
                {
                    "node": "2.6.2",
                    "distance": 19416
                },
                {
                    "node": "2.6.3",
                    "distance": 19416
                },
                {
                    "node": "2.6.4",
                    "distance": 19416
                },
                {
                    "node": "2.7.1",
                    "distance": 22588
                },
                {
                    "node": "2.7.2",
                    "distance": 22588
                },
                {
                    "node": "2.7.3",
                    "distance": 22588
                },
                {
                    "node": "2.7.4",
                    "distance": 22588
                }
            ]
        },
        {
            "3.5": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 19704
                },
                {
                    "node": "1.6.2",
                    "distance": 19704
                },
                {
                    "node": "1.6.3",
                    "distance": 19704
                },
                {
                    "node": "1.6.4",
                    "distance": 19704
                },
                {
                    "node": "1.7.1",
                    "distance": 22876
                },
                {
                    "node": "1.7.2",
                    "distance": 22876
                },
                {
                    "node": "1.7.3",
                    "distance": 22876
                },
                {
                    "node": "1.7.4",
                    "distance": 22876
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 19416
                },
                {
                    "node": "2.6.2",
                    "distance": 19416
                },
                {
                    "node": "2.6.3",
                    "distance": 19416
                },
                {
                    "node": "2.6.4",
                    "distance": 19416
                },
                {
                    "node": "2.7.1",
                    "distance": 22588
                },
                {
                    "node": "2.7.2",
                    "distance": 22588
                },
                {
                    "node": "2.7.3",
                    "distance": 22588
                },
                {
                    "node": "2.7.4",
                    "distance": 22588
                }
            ]
        },
        {
            "3.6": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 19704
                },
                {
                    "node": "1.6.2",
                    "distance": 19704
                },
                {
                    "node": "1.6.3",
                    "distance": 19704
                },
                {
                    "node": "1.6.4",
                    "distance": 19704
                },
                {
                    "node": "1.7.1",
                    "distance": 22876
                },
                {
                    "node": "1.7.2",
                    "distance": 22876
                },
                {
                    "node": "1.7.3",
                    "distance": 22876
                },
                {
                    "node": "1.7.4",
                    "distance": 22876
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 19416
                },
                {
                    "node": "2.6.2",
                    "distance": 19416
                },
                {
                    "node": "2.6.3",
                    "distance": 19416
                },
                {
                    "node": "2.6.4",
                    "distance": 19416
                },
                {
                    "node": "2.7.1",
                    "distance": 22588
                },
                {
                    "node": "2.7.2",
                    "distance": 22588
                },
                {
                    "node": "2.7.3",
                    "distance": 22588
                },
                {
                    "node": "2.7.4",
                    "distance": 22588
                }
            ]
        },
        {
            "4.1": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 19704
                },
                {
                    "node": "1.6.2",
                    "distance": 19704
                },
                {
                    "node": "1.6.3",
                    "distance": 19704
                },
                {
                    "node": "1.6.4",
                    "distance": 19704
                },
                {
                    "node": "1.7.1",
                    "distance": 22876
                },
                {
                    "node": "1.7.2",
                    "distance": 22876
                },
                {
                    "node": "1.7.3",
                    "distance": 22876
                },
                {
                    "node": "1.7.4",
                    "distance": 22876
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 19416
                },
                {
                    "node": "2.6.2",
                    "distance": 19416
                },
                {
                    "node": "2.6.3",
                    "distance": 19416
                },
                {
                    "node": "2.6.4",
                    "distance": 19416
                },
                {
                    "node": "2.7.1",
                    "distance": 22588
                },
                {
                    "node": "2.7.2",
                    "distance": 22588
                },
                {
                    "node": "2.7.3",
                    "distance": 22588
                },
                {
                    "node": "2.7.4",
                    "distance": 22588
                }
            ]
        },
        {
            "4.2": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 19704
                },
                {
                    "node": "1.6.2",
                    "distance": 19704
                },
                {
                    "node": "1.6.3",
                    "distance": 19704
                },
                {
                    "node": "1.6.4",
                    "distance": 19704
                },
                {
                    "node": "1.7.1",
                    "distance": 22876
                },
                {
                    "node": "1.7.2",
                    "distance": 22876
                },
                {
                    "node": "1.7.3",
                    "distance": 22876
                },
                {
                    "node": "1.7.4",
                    "distance": 22876
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 19416
                },
                {
                    "node": "2.6.2",
                    "distance": 19416
                },
                {
                    "node": "2.6.3",
                    "distance": 19416
                },
                {
                    "node": "2.6.4",
                    "distance": 19416
                },
                {
                    "node": "2.7.1",
                    "distance": 22588
                },
                {
                    "node": "2.7.2",
                    "distance": 22588
                },
                {
                    "node": "2.7.3",
                    "distance": 22588
                },
                {
                    "node": "2.7.4",
                    "distance": 22588
                }
            ]
        },
        {
            "4.3": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 19704
                },
                {
                    "node": "1.6.2",
                    "distance": 19704
                },
                {
                    "node": "1.6.3",
                    "distance": 19704
                },
                {
                    "node": "1.6.4",
                    "distance": 19704
                },
                {
                    "node": "1.7.1",
                    "distance": 22876
                },
                {
                    "node": "1.7.2",
                    "distance": 22876
                },
                {
                    "node": "1.7.3",
                    "distance": 22876
                },
                {
                    "node": "1.7.4",
                    "distance": 22876
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 19416
                },
                {
                    "node": "2.6.2",
                    "distance": 19416
                },
                {
                    "node": "2.6.3",
                    "distance": 19416
                },
                {
                    "node": "2.6.4",
                    "distance": 19416
                },
                {
                    "node": "2.7.1",
                    "distance": 22588
                },
                {
                    "node": "2.7.2",
                    "distance": 22588
                },
                {
                    "node": "2.7.3",
                    "distance": 22588
                },
                {
                    "node": "2.7.4",
                    "distance": 22588
                }
            ]
        },
        {
            "4.4": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 19704
                },
                {
                    "node": "1.6.2",
                    "distance": 19704
                },
                {
                    "node": "1.6.3",
                    "distance": 19704
                },
                {
                    "node": "1.6.4",
                    "distance": 19704
                },
                {
                    "node": "1.7.1",
                    "distance": 22876
                },
                {
                    "node": "1.7.2",
                    "distance": 22876
                },
                {
                    "node": "1.7.3",
                    "distance": 22876
                },
                {
                    "node": "1.7.4",
                    "distance": 22876
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 19416
                },
                {
                    "node": "2.6.2",
                    "distance": 19416
                },
                {
                    "node": "2.6.3",
                    "distance": 19416
                },
                {
                    "node": "2.6.4",
                    "distance": 19416
                },
                {
                    "node": "2.7.1",
                    "distance": 22588
                },
                {
                    "node": "2.7.2",
                    "distance": 22588
                },
                {
                    "node": "2.7.3",
                    "distance": 22588
                },
                {
                    "node": "2.7.4",
                    "distance": 22588
                }
            ]
        },
        {
            "4.5": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 19704
                },
                {
                    "node": "1.6.2",
                    "distance": 19704
                },
                {
                    "node": "1.6.3",
                    "distance": 19704
                },
                {
                    "node": "1.6.4",
                    "distance": 19704
                },
                {
                    "node": "1.7.1",
                    "distance": 22876
                },
                {
                    "node": "1.7.2",
                    "distance": 22876
                },
                {
                    "node": "1.7.3",
                    "distance": 22876
                },
                {
                    "node": "1.7.4",
                    "distance": 22876
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 19416
                },
                {
                    "node": "2.6.2",
                    "distance": 19416
                },
                {
                    "node": "2.6.3",
                    "distance": 19416
                },
                {
                    "node": "2.6.4",
                    "distance": 19416
                },
                {
                    "node": "2.7.1",
                    "distance": 22588
                },
                {
                    "node": "2.7.2",
                    "distance": 22588
                },
                {
                    "node": "2.7.3",
                    "distance": 22588
                },
                {
                    "node": "2.7.4",
                    "distance": 22588
                }
            ]
        },
        {
            "4.6": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 19704
                },
                {
                    "node": "1.6.2",
                    "distance": 19704
                },
                {
                    "node": "1.6.3",
                    "distance": 19704
                },
                {
                    "node": "1.6.4",
                    "distance": 19704
                },
                {
                    "node": "1.7.1",
                    "distance": 22876
                },
                {
                    "node": "1.7.2",
                    "distance": 22876
                },
                {
                    "node": "1.7.3",
                    "distance": 22876
                },
                {
                    "node": "1.7.4",
                    "distance": 22876
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 19416
                },
                {
                    "node": "2.6.2",
                    "distance": 19416
                },
                {
                    "node": "2.6.3",
                    "distance": 19416
                },
                {
                    "node": "2.6.4",
                    "distance": 19416
                },
                {
                    "node": "2.7.1",
                    "distance": 22588
                },
                {
                    "node": "2.7.2",
                    "distance": 22588
                },
                {
                    "node": "2.7.3",
                    "distance": 22588
                },
                {
                    "node": "2.7.4",
                    "distance": 22588
                }
            ]
        }
    ],
    "3.1": [
        {
            "1.1": [
                {
                    "node": "1.1.1",
                    "distance": 22876
                },
                {
                    "node": "1.1.2",
                    "distance": 22876
                },
                {
                    "node": "1.1.3",
                    "distance": 22876
                },
                {
                    "node": "1.1.4",
                    "distance": 22876
                },
                {
                    "node": "1.2.1",
                    "distance": 19704
                },
                {
                    "node": "1.2.2",
                    "distance": 19704
                },
                {
                    "node": "1.2.3",
                    "distance": 19704
                },
                {
                    "node": "1.2.4",
                    "distance": 19704
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 22588
                },
                {
                    "node": "2.1.2",
                    "distance": 22588
                },
                {
                    "node": "2.1.3",
                    "distance": 22588
                },
                {
                    "node": "2.1.4",
                    "distance": 22588
                },
                {
                    "node": "2.2.1",
                    "distance": 19416
                },
                {
                    "node": "2.2.2",
                    "distance": 19416
                },
                {
                    "node": "2.2.3",
                    "distance": 19416
                },
                {
                    "node": "2.2.4",
                    "distance": 19416
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "1.2": [
                {
                    "node": "1.1.1",
                    "distance": 22876
                },
                {
                    "node": "1.1.2",
                    "distance": 22876
                },
                {
                    "node": "1.1.3",
                    "distance": 22876
                },
                {
                    "node": "1.1.4",
                    "distance": 22876
                },
                {
                    "node": "1.2.1",
                    "distance": 19704
                },
                {
                    "node": "1.2.2",
                    "distance": 19704
                },
                {
                    "node": "1.2.3",
                    "distance": 19704
                },
                {
                    "node": "1.2.4",
                    "distance": 19704
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 22588
                },
                {
                    "node": "2.1.2",
                    "distance": 22588
                },
                {
                    "node": "2.1.3",
                    "distance": 22588
                },
                {
                    "node": "2.1.4",
                    "distance": 22588
                },
                {
                    "node": "2.2.1",
                    "distance": 19416
                },
                {
                    "node": "2.2.2",
                    "distance": 19416
                },
                {
                    "node": "2.2.3",
                    "distance": 19416
                },
                {
                    "node": "2.2.4",
                    "distance": 19416
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "1.3": [
                {
                    "node": "1.1.1",
                    "distance": 22876
                },
                {
                    "node": "1.1.2",
                    "distance": 22876
                },
                {
                    "node": "1.1.3",
                    "distance": 22876
                },
                {
                    "node": "1.1.4",
                    "distance": 22876
                },
                {
                    "node": "1.2.1",
                    "distance": 19704
                },
                {
                    "node": "1.2.2",
                    "distance": 19704
                },
                {
                    "node": "1.2.3",
                    "distance": 19704
                },
                {
                    "node": "1.2.4",
                    "distance": 19704
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 22588
                },
                {
                    "node": "2.1.2",
                    "distance": 22588
                },
                {
                    "node": "2.1.3",
                    "distance": 22588
                },
                {
                    "node": "2.1.4",
                    "distance": 22588
                },
                {
                    "node": "2.2.1",
                    "distance": 19416
                },
                {
                    "node": "2.2.2",
                    "distance": 19416
                },
                {
                    "node": "2.2.3",
                    "distance": 19416
                },
                {
                    "node": "2.2.4",
                    "distance": 19416
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "1.4": [
                {
                    "node": "1.1.1",
                    "distance": 22876
                },
                {
                    "node": "1.1.2",
                    "distance": 22876
                },
                {
                    "node": "1.1.3",
                    "distance": 22876
                },
                {
                    "node": "1.1.4",
                    "distance": 22876
                },
                {
                    "node": "1.2.1",
                    "distance": 19704
                },
                {
                    "node": "1.2.2",
                    "distance": 19704
                },
                {
                    "node": "1.2.3",
                    "distance": 19704
                },
                {
                    "node": "1.2.4",
                    "distance": 19704
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 22588
                },
                {
                    "node": "2.1.2",
                    "distance": 22588
                },
                {
                    "node": "2.1.3",
                    "distance": 22588
                },
                {
                    "node": "2.1.4",
                    "distance": 22588
                },
                {
                    "node": "2.2.1",
                    "distance": 19416
                },
                {
                    "node": "2.2.2",
                    "distance": 19416
                },
                {
                    "node": "2.2.3",
                    "distance": 19416
                },
                {
                    "node": "2.2.4",
                    "distance": 19416
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "1.5": [
                {
                    "node": "1.1.1",
                    "distance": 22876
                },
                {
                    "node": "1.1.2",
                    "distance": 22876
                },
                {
                    "node": "1.1.3",
                    "distance": 22876
                },
                {
                    "node": "1.1.4",
                    "distance": 22876
                },
                {
                    "node": "1.2.1",
                    "distance": 19704
                },
                {
                    "node": "1.2.2",
                    "distance": 19704
                },
                {
                    "node": "1.2.3",
                    "distance": 19704
                },
                {
                    "node": "1.2.4",
                    "distance": 19704
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 22588
                },
                {
                    "node": "2.1.2",
                    "distance": 22588
                },
                {
                    "node": "2.1.3",
                    "distance": 22588
                },
                {
                    "node": "2.1.4",
                    "distance": 22588
                },
                {
                    "node": "2.2.1",
                    "distance": 19416
                },
                {
                    "node": "2.2.2",
                    "distance": 19416
                },
                {
                    "node": "2.2.3",
                    "distance": 19416
                },
                {
                    "node": "2.2.4",
                    "distance": 19416
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "1.6": [
                {
                    "node": "1.1.1",
                    "distance": 22876
                },
                {
                    "node": "1.1.2",
                    "distance": 22876
                },
                {
                    "node": "1.1.3",
                    "distance": 22876
                },
                {
                    "node": "1.1.4",
                    "distance": 22876
                },
                {
                    "node": "1.2.1",
                    "distance": 19704
                },
                {
                    "node": "1.2.2",
                    "distance": 19704
                },
                {
                    "node": "1.2.3",
                    "distance": 19704
                },
                {
                    "node": "1.2.4",
                    "distance": 19704
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 22588
                },
                {
                    "node": "2.1.2",
                    "distance": 22588
                },
                {
                    "node": "2.1.3",
                    "distance": 22588
                },
                {
                    "node": "2.1.4",
                    "distance": 22588
                },
                {
                    "node": "2.2.1",
                    "distance": 19416
                },
                {
                    "node": "2.2.2",
                    "distance": 19416
                },
                {
                    "node": "2.2.3",
                    "distance": 19416
                },
                {
                    "node": "2.2.4",
                    "distance": 19416
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "2.1": [
                {
                    "node": "1.1.1",
                    "distance": 22876
                },
                {
                    "node": "1.1.2",
                    "distance": 22876
                },
                {
                    "node": "1.1.3",
                    "distance": 22876
                },
                {
                    "node": "1.1.4",
                    "distance": 22876
                },
                {
                    "node": "1.2.1",
                    "distance": 19704
                },
                {
                    "node": "1.2.2",
                    "distance": 19704
                },
                {
                    "node": "1.2.3",
                    "distance": 19704
                },
                {
                    "node": "1.2.4",
                    "distance": 19704
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 18522
                },
                {
                    "node": "1.4.2",
                    "distance": 18522
                },
                {
                    "node": "1.4.3",
                    "distance": 18522
                },
                {
                    "node": "1.4.4",
                    "distance": 18522
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 19704
                },
                {
                    "node": "1.6.2",
                    "distance": 19704
                },
                {
                    "node": "1.6.3",
                    "distance": 19704
                },
                {
                    "node": "1.6.4",
                    "distance": 19704
                },
                {
                    "node": "1.7.1",
                    "distance": 22876
                },
                {
                    "node": "1.7.2",
                    "distance": 22876
                },
                {
                    "node": "1.7.3",
                    "distance": 22876
                },
                {
                    "node": "1.7.4",
                    "distance": 22876
                },
                {
                    "node": "2.1.1",
                    "distance": 22588
                },
                {
                    "node": "2.1.2",
                    "distance": 22588
                },
                {
                    "node": "2.1.3",
                    "distance": 22588
                },
                {
                    "node": "2.1.4",
                    "distance": 22588
                },
                {
                    "node": "2.2.1",
                    "distance": 19416
                },
                {
                    "node": "2.2.2",
                    "distance": 19416
                },
                {
                    "node": "2.2.3",
                    "distance": 19416
                },
                {
                    "node": "2.2.4",
                    "distance": 19416
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 17946
                },
                {
                    "node": "2.4.2",
                    "distance": 17946
                },
                {
                    "node": "2.4.3",
                    "distance": 17946
                },
                {
                    "node": "2.4.4",
                    "distance": 17946
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 19416
                },
                {
                    "node": "2.6.2",
                    "distance": 19416
                },
                {
                    "node": "2.6.3",
                    "distance": 19416
                },
                {
                    "node": "2.6.4",
                    "distance": 19416
                },
                {
                    "node": "2.7.1",
                    "distance": 22588
                },
                {
                    "node": "2.7.2",
                    "distance": 22588
                },
                {
                    "node": "2.7.3",
                    "distance": 22588
                },
                {
                    "node": "2.7.4",
                    "distance": 22588
                }
            ]
        },
        {
            "2.2": [
                {
                    "node": "1.1.1",
                    "distance": 22876
                },
                {
                    "node": "1.1.2",
                    "distance": 22876
                },
                {
                    "node": "1.1.3",
                    "distance": 22876
                },
                {
                    "node": "1.1.4",
                    "distance": 22876
                },
                {
                    "node": "1.2.1",
                    "distance": 19704
                },
                {
                    "node": "1.2.2",
                    "distance": 19704
                },
                {
                    "node": "1.2.3",
                    "distance": 19704
                },
                {
                    "node": "1.2.4",
                    "distance": 19704
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 18522
                },
                {
                    "node": "1.4.2",
                    "distance": 18522
                },
                {
                    "node": "1.4.3",
                    "distance": 18522
                },
                {
                    "node": "1.4.4",
                    "distance": 18522
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 19704
                },
                {
                    "node": "1.6.2",
                    "distance": 19704
                },
                {
                    "node": "1.6.3",
                    "distance": 19704
                },
                {
                    "node": "1.6.4",
                    "distance": 19704
                },
                {
                    "node": "1.7.1",
                    "distance": 22876
                },
                {
                    "node": "1.7.2",
                    "distance": 22876
                },
                {
                    "node": "1.7.3",
                    "distance": 22876
                },
                {
                    "node": "1.7.4",
                    "distance": 22876
                },
                {
                    "node": "2.1.1",
                    "distance": 22588
                },
                {
                    "node": "2.1.2",
                    "distance": 22588
                },
                {
                    "node": "2.1.3",
                    "distance": 22588
                },
                {
                    "node": "2.1.4",
                    "distance": 22588
                },
                {
                    "node": "2.2.1",
                    "distance": 19416
                },
                {
                    "node": "2.2.2",
                    "distance": 19416
                },
                {
                    "node": "2.2.3",
                    "distance": 19416
                },
                {
                    "node": "2.2.4",
                    "distance": 19416
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 17946
                },
                {
                    "node": "2.4.2",
                    "distance": 17946
                },
                {
                    "node": "2.4.3",
                    "distance": 17946
                },
                {
                    "node": "2.4.4",
                    "distance": 17946
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 19416
                },
                {
                    "node": "2.6.2",
                    "distance": 19416
                },
                {
                    "node": "2.6.3",
                    "distance": 19416
                },
                {
                    "node": "2.6.4",
                    "distance": 19416
                },
                {
                    "node": "2.7.1",
                    "distance": 22588
                },
                {
                    "node": "2.7.2",
                    "distance": 22588
                },
                {
                    "node": "2.7.3",
                    "distance": 22588
                },
                {
                    "node": "2.7.4",
                    "distance": 22588
                }
            ]
        },
        {
            "2.3": [
                {
                    "node": "1.1.1",
                    "distance": 22876
                },
                {
                    "node": "1.1.2",
                    "distance": 22876
                },
                {
                    "node": "1.1.3",
                    "distance": 22876
                },
                {
                    "node": "1.1.4",
                    "distance": 22876
                },
                {
                    "node": "1.2.1",
                    "distance": 19704
                },
                {
                    "node": "1.2.2",
                    "distance": 19704
                },
                {
                    "node": "1.2.3",
                    "distance": 19704
                },
                {
                    "node": "1.2.4",
                    "distance": 19704
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 18522
                },
                {
                    "node": "1.4.2",
                    "distance": 18522
                },
                {
                    "node": "1.4.3",
                    "distance": 18522
                },
                {
                    "node": "1.4.4",
                    "distance": 18522
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 19704
                },
                {
                    "node": "1.6.2",
                    "distance": 19704
                },
                {
                    "node": "1.6.3",
                    "distance": 19704
                },
                {
                    "node": "1.6.4",
                    "distance": 19704
                },
                {
                    "node": "1.7.1",
                    "distance": 22876
                },
                {
                    "node": "1.7.2",
                    "distance": 22876
                },
                {
                    "node": "1.7.3",
                    "distance": 22876
                },
                {
                    "node": "1.7.4",
                    "distance": 22876
                },
                {
                    "node": "2.1.1",
                    "distance": 22588
                },
                {
                    "node": "2.1.2",
                    "distance": 22588
                },
                {
                    "node": "2.1.3",
                    "distance": 22588
                },
                {
                    "node": "2.1.4",
                    "distance": 22588
                },
                {
                    "node": "2.2.1",
                    "distance": 19416
                },
                {
                    "node": "2.2.2",
                    "distance": 19416
                },
                {
                    "node": "2.2.3",
                    "distance": 19416
                },
                {
                    "node": "2.2.4",
                    "distance": 19416
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 17946
                },
                {
                    "node": "2.4.2",
                    "distance": 17946
                },
                {
                    "node": "2.4.3",
                    "distance": 17946
                },
                {
                    "node": "2.4.4",
                    "distance": 17946
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 19416
                },
                {
                    "node": "2.6.2",
                    "distance": 19416
                },
                {
                    "node": "2.6.3",
                    "distance": 19416
                },
                {
                    "node": "2.6.4",
                    "distance": 19416
                },
                {
                    "node": "2.7.1",
                    "distance": 22588
                },
                {
                    "node": "2.7.2",
                    "distance": 22588
                },
                {
                    "node": "2.7.3",
                    "distance": 22588
                },
                {
                    "node": "2.7.4",
                    "distance": 22588
                }
            ]
        },
        {
            "2.4": [
                {
                    "node": "1.1.1",
                    "distance": 22876
                },
                {
                    "node": "1.1.2",
                    "distance": 22876
                },
                {
                    "node": "1.1.3",
                    "distance": 22876
                },
                {
                    "node": "1.1.4",
                    "distance": 22876
                },
                {
                    "node": "1.2.1",
                    "distance": 19704
                },
                {
                    "node": "1.2.2",
                    "distance": 19704
                },
                {
                    "node": "1.2.3",
                    "distance": 19704
                },
                {
                    "node": "1.2.4",
                    "distance": 19704
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 18522
                },
                {
                    "node": "1.4.2",
                    "distance": 18522
                },
                {
                    "node": "1.4.3",
                    "distance": 18522
                },
                {
                    "node": "1.4.4",
                    "distance": 18522
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 19704
                },
                {
                    "node": "1.6.2",
                    "distance": 19704
                },
                {
                    "node": "1.6.3",
                    "distance": 19704
                },
                {
                    "node": "1.6.4",
                    "distance": 19704
                },
                {
                    "node": "1.7.1",
                    "distance": 22876
                },
                {
                    "node": "1.7.2",
                    "distance": 22876
                },
                {
                    "node": "1.7.3",
                    "distance": 22876
                },
                {
                    "node": "1.7.4",
                    "distance": 22876
                },
                {
                    "node": "2.1.1",
                    "distance": 22588
                },
                {
                    "node": "2.1.2",
                    "distance": 22588
                },
                {
                    "node": "2.1.3",
                    "distance": 22588
                },
                {
                    "node": "2.1.4",
                    "distance": 22588
                },
                {
                    "node": "2.2.1",
                    "distance": 19416
                },
                {
                    "node": "2.2.2",
                    "distance": 19416
                },
                {
                    "node": "2.2.3",
                    "distance": 19416
                },
                {
                    "node": "2.2.4",
                    "distance": 19416
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 17946
                },
                {
                    "node": "2.4.2",
                    "distance": 17946
                },
                {
                    "node": "2.4.3",
                    "distance": 17946
                },
                {
                    "node": "2.4.4",
                    "distance": 17946
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 19416
                },
                {
                    "node": "2.6.2",
                    "distance": 19416
                },
                {
                    "node": "2.6.3",
                    "distance": 19416
                },
                {
                    "node": "2.6.4",
                    "distance": 19416
                },
                {
                    "node": "2.7.1",
                    "distance": 22588
                },
                {
                    "node": "2.7.2",
                    "distance": 22588
                },
                {
                    "node": "2.7.3",
                    "distance": 22588
                },
                {
                    "node": "2.7.4",
                    "distance": 22588
                }
            ]
        },
        {
            "2.5": [
                {
                    "node": "1.1.1",
                    "distance": 27230
                },
                {
                    "node": "1.1.2",
                    "distance": 27230
                },
                {
                    "node": "1.1.3",
                    "distance": 27230
                },
                {
                    "node": "1.1.4",
                    "distance": 27230
                },
                {
                    "node": "1.2.1",
                    "distance": 20886
                },
                {
                    "node": "1.2.2",
                    "distance": 20886
                },
                {
                    "node": "1.2.3",
                    "distance": 20886
                },
                {
                    "node": "1.2.4",
                    "distance": 20886
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 18522
                },
                {
                    "node": "1.4.2",
                    "distance": 18522
                },
                {
                    "node": "1.4.3",
                    "distance": 18522
                },
                {
                    "node": "1.4.4",
                    "distance": 18522
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 27230
                },
                {
                    "node": "2.1.2",
                    "distance": 27230
                },
                {
                    "node": "2.1.3",
                    "distance": 27230
                },
                {
                    "node": "2.1.4",
                    "distance": 27230
                },
                {
                    "node": "2.2.1",
                    "distance": 20886
                },
                {
                    "node": "2.2.2",
                    "distance": 20886
                },
                {
                    "node": "2.2.3",
                    "distance": 20886
                },
                {
                    "node": "2.2.4",
                    "distance": 20886
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 17946
                },
                {
                    "node": "2.4.2",
                    "distance": 17946
                },
                {
                    "node": "2.4.3",
                    "distance": 17946
                },
                {
                    "node": "2.4.4",
                    "distance": 17946
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "2.6": [
                {
                    "node": "1.1.1",
                    "distance": 27230
                },
                {
                    "node": "1.1.2",
                    "distance": 27230
                },
                {
                    "node": "1.1.3",
                    "distance": 27230
                },
                {
                    "node": "1.1.4",
                    "distance": 27230
                },
                {
                    "node": "1.2.1",
                    "distance": 20886
                },
                {
                    "node": "1.2.2",
                    "distance": 20886
                },
                {
                    "node": "1.2.3",
                    "distance": 20886
                },
                {
                    "node": "1.2.4",
                    "distance": 20886
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 18522
                },
                {
                    "node": "1.4.2",
                    "distance": 18522
                },
                {
                    "node": "1.4.3",
                    "distance": 18522
                },
                {
                    "node": "1.4.4",
                    "distance": 18522
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 27230
                },
                {
                    "node": "2.1.2",
                    "distance": 27230
                },
                {
                    "node": "2.1.3",
                    "distance": 27230
                },
                {
                    "node": "2.1.4",
                    "distance": 27230
                },
                {
                    "node": "2.2.1",
                    "distance": 20886
                },
                {
                    "node": "2.2.2",
                    "distance": 20886
                },
                {
                    "node": "2.2.3",
                    "distance": 20886
                },
                {
                    "node": "2.2.4",
                    "distance": 20886
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 17946
                },
                {
                    "node": "2.4.2",
                    "distance": 17946
                },
                {
                    "node": "2.4.3",
                    "distance": 17946
                },
                {
                    "node": "2.4.4",
                    "distance": 17946
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "3.1": [
                {
                    "node": "1.1.1",
                    "distance": 27230
                },
                {
                    "node": "1.1.2",
                    "distance": 27230
                },
                {
                    "node": "1.1.3",
                    "distance": 27230
                },
                {
                    "node": "1.1.4",
                    "distance": 27230
                },
                {
                    "node": "1.2.1",
                    "distance": 20886
                },
                {
                    "node": "1.2.2",
                    "distance": 20886
                },
                {
                    "node": "1.2.3",
                    "distance": 20886
                },
                {
                    "node": "1.2.4",
                    "distance": 20886
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 18522
                },
                {
                    "node": "1.4.2",
                    "distance": 18522
                },
                {
                    "node": "1.4.3",
                    "distance": 18522
                },
                {
                    "node": "1.4.4",
                    "distance": 18522
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 27230
                },
                {
                    "node": "2.1.2",
                    "distance": 27230
                },
                {
                    "node": "2.1.3",
                    "distance": 27230
                },
                {
                    "node": "2.1.4",
                    "distance": 27230
                },
                {
                    "node": "2.2.1",
                    "distance": 20886
                },
                {
                    "node": "2.2.2",
                    "distance": 20886
                },
                {
                    "node": "2.2.3",
                    "distance": 20886
                },
                {
                    "node": "2.2.4",
                    "distance": 20886
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 17946
                },
                {
                    "node": "2.4.2",
                    "distance": 17946
                },
                {
                    "node": "2.4.3",
                    "distance": 17946
                },
                {
                    "node": "2.4.4",
                    "distance": 17946
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "3.2": [
                {
                    "node": "1.1.1",
                    "distance": 27230
                },
                {
                    "node": "1.1.2",
                    "distance": 27230
                },
                {
                    "node": "1.1.3",
                    "distance": 27230
                },
                {
                    "node": "1.1.4",
                    "distance": 27230
                },
                {
                    "node": "1.2.1",
                    "distance": 20886
                },
                {
                    "node": "1.2.2",
                    "distance": 20886
                },
                {
                    "node": "1.2.3",
                    "distance": 20886
                },
                {
                    "node": "1.2.4",
                    "distance": 20886
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 18522
                },
                {
                    "node": "1.4.2",
                    "distance": 18522
                },
                {
                    "node": "1.4.3",
                    "distance": 18522
                },
                {
                    "node": "1.4.4",
                    "distance": 18522
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 27230
                },
                {
                    "node": "2.1.2",
                    "distance": 27230
                },
                {
                    "node": "2.1.3",
                    "distance": 27230
                },
                {
                    "node": "2.1.4",
                    "distance": 27230
                },
                {
                    "node": "2.2.1",
                    "distance": 20886
                },
                {
                    "node": "2.2.2",
                    "distance": 20886
                },
                {
                    "node": "2.2.3",
                    "distance": 20886
                },
                {
                    "node": "2.2.4",
                    "distance": 20886
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 17946
                },
                {
                    "node": "2.4.2",
                    "distance": 17946
                },
                {
                    "node": "2.4.3",
                    "distance": 17946
                },
                {
                    "node": "2.4.4",
                    "distance": 17946
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "3.3": [
                {
                    "node": "1.1.1",
                    "distance": 27230
                },
                {
                    "node": "1.1.2",
                    "distance": 27230
                },
                {
                    "node": "1.1.3",
                    "distance": 27230
                },
                {
                    "node": "1.1.4",
                    "distance": 27230
                },
                {
                    "node": "1.2.1",
                    "distance": 20886
                },
                {
                    "node": "1.2.2",
                    "distance": 20886
                },
                {
                    "node": "1.2.3",
                    "distance": 20886
                },
                {
                    "node": "1.2.4",
                    "distance": 20886
                },
                {
                    "node": "1.3.1",
                    "distance": 18522
                },
                {
                    "node": "1.3.2",
                    "distance": 18522
                },
                {
                    "node": "1.3.3",
                    "distance": 18522
                },
                {
                    "node": "1.3.4",
                    "distance": 18522
                },
                {
                    "node": "1.4.1",
                    "distance": 18522
                },
                {
                    "node": "1.4.2",
                    "distance": 18522
                },
                {
                    "node": "1.4.3",
                    "distance": 18522
                },
                {
                    "node": "1.4.4",
                    "distance": 18522
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 27230
                },
                {
                    "node": "2.1.2",
                    "distance": 27230
                },
                {
                    "node": "2.1.3",
                    "distance": 27230
                },
                {
                    "node": "2.1.4",
                    "distance": 27230
                },
                {
                    "node": "2.2.1",
                    "distance": 20886
                },
                {
                    "node": "2.2.2",
                    "distance": 20886
                },
                {
                    "node": "2.2.3",
                    "distance": 20886
                },
                {
                    "node": "2.2.4",
                    "distance": 20886
                },
                {
                    "node": "2.3.1",
                    "distance": 17946
                },
                {
                    "node": "2.3.2",
                    "distance": 17946
                },
                {
                    "node": "2.3.3",
                    "distance": 17946
                },
                {
                    "node": "2.3.4",
                    "distance": 17946
                },
                {
                    "node": "2.4.1",
                    "distance": 17946
                },
                {
                    "node": "2.4.2",
                    "distance": 17946
                },
                {
                    "node": "2.4.3",
                    "distance": 17946
                },
                {
                    "node": "2.4.4",
                    "distance": 17946
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "3.4": [
                {
                    "node": "1.1.1",
                    "distance": 33670
                },
                {
                    "node": "1.1.2",
                    "distance": 33670
                },
                {
                    "node": "1.1.3",
                    "distance": 33670
                },
                {
                    "node": "1.1.4",
                    "distance": 33670
                },
                {
                    "node": "1.2.1",
                    "distance": 27257
                },
                {
                    "node": "1.2.2",
                    "distance": 27257
                },
                {
                    "node": "1.2.3",
                    "distance": 27257
                },
                {
                    "node": "1.2.4",
                    "distance": 27257
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 33670
                },
                {
                    "node": "2.1.2",
                    "distance": 33670
                },
                {
                    "node": "2.1.3",
                    "distance": 33670
                },
                {
                    "node": "2.1.4",
                    "distance": 33670
                },
                {
                    "node": "2.2.1",
                    "distance": 27257
                },
                {
                    "node": "2.2.2",
                    "distance": 27257
                },
                {
                    "node": "2.2.3",
                    "distance": 27257
                },
                {
                    "node": "2.2.4",
                    "distance": 27257
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "3.5": [
                {
                    "node": "1.1.1",
                    "distance": 33670
                },
                {
                    "node": "1.1.2",
                    "distance": 33670
                },
                {
                    "node": "1.1.3",
                    "distance": 33670
                },
                {
                    "node": "1.1.4",
                    "distance": 33670
                },
                {
                    "node": "1.2.1",
                    "distance": 27257
                },
                {
                    "node": "1.2.2",
                    "distance": 27257
                },
                {
                    "node": "1.2.3",
                    "distance": 27257
                },
                {
                    "node": "1.2.4",
                    "distance": 27257
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 33670
                },
                {
                    "node": "2.1.2",
                    "distance": 33670
                },
                {
                    "node": "2.1.3",
                    "distance": 33670
                },
                {
                    "node": "2.1.4",
                    "distance": 33670
                },
                {
                    "node": "2.2.1",
                    "distance": 27257
                },
                {
                    "node": "2.2.2",
                    "distance": 27257
                },
                {
                    "node": "2.2.3",
                    "distance": 27257
                },
                {
                    "node": "2.2.4",
                    "distance": 27257
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "3.6": [
                {
                    "node": "1.1.1",
                    "distance": 33670
                },
                {
                    "node": "1.1.2",
                    "distance": 33670
                },
                {
                    "node": "1.1.3",
                    "distance": 33670
                },
                {
                    "node": "1.1.4",
                    "distance": 33670
                },
                {
                    "node": "1.2.1",
                    "distance": 27257
                },
                {
                    "node": "1.2.2",
                    "distance": 27257
                },
                {
                    "node": "1.2.3",
                    "distance": 27257
                },
                {
                    "node": "1.2.4",
                    "distance": 27257
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 33670
                },
                {
                    "node": "2.1.2",
                    "distance": 33670
                },
                {
                    "node": "2.1.3",
                    "distance": 33670
                },
                {
                    "node": "2.1.4",
                    "distance": 33670
                },
                {
                    "node": "2.2.1",
                    "distance": 27257
                },
                {
                    "node": "2.2.2",
                    "distance": 27257
                },
                {
                    "node": "2.2.3",
                    "distance": 27257
                },
                {
                    "node": "2.2.4",
                    "distance": 27257
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "4.1": [
                {
                    "node": "1.1.1",
                    "distance": 33670
                },
                {
                    "node": "1.1.2",
                    "distance": 33670
                },
                {
                    "node": "1.1.3",
                    "distance": 33670
                },
                {
                    "node": "1.1.4",
                    "distance": 33670
                },
                {
                    "node": "1.2.1",
                    "distance": 27257
                },
                {
                    "node": "1.2.2",
                    "distance": 27257
                },
                {
                    "node": "1.2.3",
                    "distance": 27257
                },
                {
                    "node": "1.2.4",
                    "distance": 27257
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 33670
                },
                {
                    "node": "2.1.2",
                    "distance": 33670
                },
                {
                    "node": "2.1.3",
                    "distance": 33670
                },
                {
                    "node": "2.1.4",
                    "distance": 33670
                },
                {
                    "node": "2.2.1",
                    "distance": 27257
                },
                {
                    "node": "2.2.2",
                    "distance": 27257
                },
                {
                    "node": "2.2.3",
                    "distance": 27257
                },
                {
                    "node": "2.2.4",
                    "distance": 27257
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "4.2": [
                {
                    "node": "1.1.1",
                    "distance": 33670
                },
                {
                    "node": "1.1.2",
                    "distance": 33670
                },
                {
                    "node": "1.1.3",
                    "distance": 33670
                },
                {
                    "node": "1.1.4",
                    "distance": 33670
                },
                {
                    "node": "1.2.1",
                    "distance": 27257
                },
                {
                    "node": "1.2.2",
                    "distance": 27257
                },
                {
                    "node": "1.2.3",
                    "distance": 27257
                },
                {
                    "node": "1.2.4",
                    "distance": 27257
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 33670
                },
                {
                    "node": "2.1.2",
                    "distance": 33670
                },
                {
                    "node": "2.1.3",
                    "distance": 33670
                },
                {
                    "node": "2.1.4",
                    "distance": 33670
                },
                {
                    "node": "2.2.1",
                    "distance": 27257
                },
                {
                    "node": "2.2.2",
                    "distance": 27257
                },
                {
                    "node": "2.2.3",
                    "distance": 27257
                },
                {
                    "node": "2.2.4",
                    "distance": 27257
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "4.3": [
                {
                    "node": "1.1.1",
                    "distance": 33670
                },
                {
                    "node": "1.1.2",
                    "distance": 33670
                },
                {
                    "node": "1.1.3",
                    "distance": 33670
                },
                {
                    "node": "1.1.4",
                    "distance": 33670
                },
                {
                    "node": "1.2.1",
                    "distance": 27257
                },
                {
                    "node": "1.2.2",
                    "distance": 27257
                },
                {
                    "node": "1.2.3",
                    "distance": 27257
                },
                {
                    "node": "1.2.4",
                    "distance": 27257
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 33670
                },
                {
                    "node": "2.1.2",
                    "distance": 33670
                },
                {
                    "node": "2.1.3",
                    "distance": 33670
                },
                {
                    "node": "2.1.4",
                    "distance": 33670
                },
                {
                    "node": "2.2.1",
                    "distance": 27257
                },
                {
                    "node": "2.2.2",
                    "distance": 27257
                },
                {
                    "node": "2.2.3",
                    "distance": 27257
                },
                {
                    "node": "2.2.4",
                    "distance": 27257
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "4.4": [
                {
                    "node": "1.1.1",
                    "distance": 33670
                },
                {
                    "node": "1.1.2",
                    "distance": 33670
                },
                {
                    "node": "1.1.3",
                    "distance": 33670
                },
                {
                    "node": "1.1.4",
                    "distance": 33670
                },
                {
                    "node": "1.2.1",
                    "distance": 27257
                },
                {
                    "node": "1.2.2",
                    "distance": 27257
                },
                {
                    "node": "1.2.3",
                    "distance": 27257
                },
                {
                    "node": "1.2.4",
                    "distance": 27257
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 33670
                },
                {
                    "node": "2.1.2",
                    "distance": 33670
                },
                {
                    "node": "2.1.3",
                    "distance": 33670
                },
                {
                    "node": "2.1.4",
                    "distance": 33670
                },
                {
                    "node": "2.2.1",
                    "distance": 27257
                },
                {
                    "node": "2.2.2",
                    "distance": 27257
                },
                {
                    "node": "2.2.3",
                    "distance": 27257
                },
                {
                    "node": "2.2.4",
                    "distance": 27257
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "4.5": [
                {
                    "node": "1.1.1",
                    "distance": 33670
                },
                {
                    "node": "1.1.2",
                    "distance": 33670
                },
                {
                    "node": "1.1.3",
                    "distance": 33670
                },
                {
                    "node": "1.1.4",
                    "distance": 33670
                },
                {
                    "node": "1.2.1",
                    "distance": 27257
                },
                {
                    "node": "1.2.2",
                    "distance": 27257
                },
                {
                    "node": "1.2.3",
                    "distance": 27257
                },
                {
                    "node": "1.2.4",
                    "distance": 27257
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 33670
                },
                {
                    "node": "2.1.2",
                    "distance": 33670
                },
                {
                    "node": "2.1.3",
                    "distance": 33670
                },
                {
                    "node": "2.1.4",
                    "distance": 33670
                },
                {
                    "node": "2.2.1",
                    "distance": 27257
                },
                {
                    "node": "2.2.2",
                    "distance": 27257
                },
                {
                    "node": "2.2.3",
                    "distance": 27257
                },
                {
                    "node": "2.2.4",
                    "distance": 27257
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "4.6": [
                {
                    "node": "1.1.1",
                    "distance": 33670
                },
                {
                    "node": "1.1.2",
                    "distance": 33670
                },
                {
                    "node": "1.1.3",
                    "distance": 33670
                },
                {
                    "node": "1.1.4",
                    "distance": 33670
                },
                {
                    "node": "1.2.1",
                    "distance": 27257
                },
                {
                    "node": "1.2.2",
                    "distance": 27257
                },
                {
                    "node": "1.2.3",
                    "distance": 27257
                },
                {
                    "node": "1.2.4",
                    "distance": 27257
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 33670
                },
                {
                    "node": "2.1.2",
                    "distance": 33670
                },
                {
                    "node": "2.1.3",
                    "distance": 33670
                },
                {
                    "node": "2.1.4",
                    "distance": 33670
                },
                {
                    "node": "2.2.1",
                    "distance": 27257
                },
                {
                    "node": "2.2.2",
                    "distance": 27257
                },
                {
                    "node": "2.2.3",
                    "distance": 27257
                },
                {
                    "node": "2.2.4",
                    "distance": 27257
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        }
    ],
    "4.1": [
        {
            "1.1": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "1.2": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "1.3": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "1.4": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "1.5": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "1.6": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 22876
                },
                {
                    "node": "1.5.2",
                    "distance": 22876
                },
                {
                    "node": "1.5.3",
                    "distance": 22876
                },
                {
                    "node": "1.5.4",
                    "distance": 22876
                },
                {
                    "node": "1.6.1",
                    "distance": 26075
                },
                {
                    "node": "1.6.2",
                    "distance": 26075
                },
                {
                    "node": "1.6.3",
                    "distance": 26075
                },
                {
                    "node": "1.6.4",
                    "distance": 26075
                },
                {
                    "node": "1.7.1",
                    "distance": 29316
                },
                {
                    "node": "1.7.2",
                    "distance": 29316
                },
                {
                    "node": "1.7.3",
                    "distance": 29316
                },
                {
                    "node": "1.7.4",
                    "distance": 29316
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 22588
                },
                {
                    "node": "2.5.2",
                    "distance": 22588
                },
                {
                    "node": "2.5.3",
                    "distance": 22588
                },
                {
                    "node": "2.5.4",
                    "distance": 22588
                },
                {
                    "node": "2.6.1",
                    "distance": 25787
                },
                {
                    "node": "2.6.2",
                    "distance": 25787
                },
                {
                    "node": "2.6.3",
                    "distance": 25787
                },
                {
                    "node": "2.6.4",
                    "distance": 25787
                },
                {
                    "node": "2.7.1",
                    "distance": 29028
                },
                {
                    "node": "2.7.2",
                    "distance": 29028
                },
                {
                    "node": "2.7.3",
                    "distance": 29028
                },
                {
                    "node": "2.7.4",
                    "distance": 29028
                }
            ]
        },
        {
            "2.1": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 19704
                },
                {
                    "node": "1.6.2",
                    "distance": 19704
                },
                {
                    "node": "1.6.3",
                    "distance": 19704
                },
                {
                    "node": "1.6.4",
                    "distance": 19704
                },
                {
                    "node": "1.7.1",
                    "distance": 22876
                },
                {
                    "node": "1.7.2",
                    "distance": 22876
                },
                {
                    "node": "1.7.3",
                    "distance": 22876
                },
                {
                    "node": "1.7.4",
                    "distance": 22876
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 19416
                },
                {
                    "node": "2.6.2",
                    "distance": 19416
                },
                {
                    "node": "2.6.3",
                    "distance": 19416
                },
                {
                    "node": "2.6.4",
                    "distance": 19416
                },
                {
                    "node": "2.7.1",
                    "distance": 22588
                },
                {
                    "node": "2.7.2",
                    "distance": 22588
                },
                {
                    "node": "2.7.3",
                    "distance": 22588
                },
                {
                    "node": "2.7.4",
                    "distance": 22588
                }
            ]
        },
        {
            "2.2": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 19704
                },
                {
                    "node": "1.6.2",
                    "distance": 19704
                },
                {
                    "node": "1.6.3",
                    "distance": 19704
                },
                {
                    "node": "1.6.4",
                    "distance": 19704
                },
                {
                    "node": "1.7.1",
                    "distance": 22876
                },
                {
                    "node": "1.7.2",
                    "distance": 22876
                },
                {
                    "node": "1.7.3",
                    "distance": 22876
                },
                {
                    "node": "1.7.4",
                    "distance": 22876
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 19416
                },
                {
                    "node": "2.6.2",
                    "distance": 19416
                },
                {
                    "node": "2.6.3",
                    "distance": 19416
                },
                {
                    "node": "2.6.4",
                    "distance": 19416
                },
                {
                    "node": "2.7.1",
                    "distance": 22588
                },
                {
                    "node": "2.7.2",
                    "distance": 22588
                },
                {
                    "node": "2.7.3",
                    "distance": 22588
                },
                {
                    "node": "2.7.4",
                    "distance": 22588
                }
            ]
        },
        {
            "2.3": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 19704
                },
                {
                    "node": "1.6.2",
                    "distance": 19704
                },
                {
                    "node": "1.6.3",
                    "distance": 19704
                },
                {
                    "node": "1.6.4",
                    "distance": 19704
                },
                {
                    "node": "1.7.1",
                    "distance": 22876
                },
                {
                    "node": "1.7.2",
                    "distance": 22876
                },
                {
                    "node": "1.7.3",
                    "distance": 22876
                },
                {
                    "node": "1.7.4",
                    "distance": 22876
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 19416
                },
                {
                    "node": "2.6.2",
                    "distance": 19416
                },
                {
                    "node": "2.6.3",
                    "distance": 19416
                },
                {
                    "node": "2.6.4",
                    "distance": 19416
                },
                {
                    "node": "2.7.1",
                    "distance": 22588
                },
                {
                    "node": "2.7.2",
                    "distance": 22588
                },
                {
                    "node": "2.7.3",
                    "distance": 22588
                },
                {
                    "node": "2.7.4",
                    "distance": 22588
                }
            ]
        },
        {
            "2.4": [
                {
                    "node": "1.1.1",
                    "distance": 29316
                },
                {
                    "node": "1.1.2",
                    "distance": 29316
                },
                {
                    "node": "1.1.3",
                    "distance": 29316
                },
                {
                    "node": "1.1.4",
                    "distance": 29316
                },
                {
                    "node": "1.2.1",
                    "distance": 26075
                },
                {
                    "node": "1.2.2",
                    "distance": 26075
                },
                {
                    "node": "1.2.3",
                    "distance": 26075
                },
                {
                    "node": "1.2.4",
                    "distance": 26075
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 19704
                },
                {
                    "node": "1.6.2",
                    "distance": 19704
                },
                {
                    "node": "1.6.3",
                    "distance": 19704
                },
                {
                    "node": "1.6.4",
                    "distance": 19704
                },
                {
                    "node": "1.7.1",
                    "distance": 22876
                },
                {
                    "node": "1.7.2",
                    "distance": 22876
                },
                {
                    "node": "1.7.3",
                    "distance": 22876
                },
                {
                    "node": "1.7.4",
                    "distance": 22876
                },
                {
                    "node": "2.1.1",
                    "distance": 29028
                },
                {
                    "node": "2.1.2",
                    "distance": 29028
                },
                {
                    "node": "2.1.3",
                    "distance": 29028
                },
                {
                    "node": "2.1.4",
                    "distance": 29028
                },
                {
                    "node": "2.2.1",
                    "distance": 25787
                },
                {
                    "node": "2.2.2",
                    "distance": 25787
                },
                {
                    "node": "2.2.3",
                    "distance": 25787
                },
                {
                    "node": "2.2.4",
                    "distance": 25787
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 19416
                },
                {
                    "node": "2.6.2",
                    "distance": 19416
                },
                {
                    "node": "2.6.3",
                    "distance": 19416
                },
                {
                    "node": "2.6.4",
                    "distance": 19416
                },
                {
                    "node": "2.7.1",
                    "distance": 22588
                },
                {
                    "node": "2.7.2",
                    "distance": 22588
                },
                {
                    "node": "2.7.3",
                    "distance": 22588
                },
                {
                    "node": "2.7.4",
                    "distance": 22588
                }
            ]
        },
        {
            "2.5": [
                {
                    "node": "1.1.1",
                    "distance": 33670
                },
                {
                    "node": "1.1.2",
                    "distance": 33670
                },
                {
                    "node": "1.1.3",
                    "distance": 33670
                },
                {
                    "node": "1.1.4",
                    "distance": 33670
                },
                {
                    "node": "1.2.1",
                    "distance": 27257
                },
                {
                    "node": "1.2.2",
                    "distance": 27257
                },
                {
                    "node": "1.2.3",
                    "distance": 27257
                },
                {
                    "node": "1.2.4",
                    "distance": 27257
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 33670
                },
                {
                    "node": "2.1.2",
                    "distance": 33670
                },
                {
                    "node": "2.1.3",
                    "distance": 33670
                },
                {
                    "node": "2.1.4",
                    "distance": 33670
                },
                {
                    "node": "2.2.1",
                    "distance": 27257
                },
                {
                    "node": "2.2.2",
                    "distance": 27257
                },
                {
                    "node": "2.2.3",
                    "distance": 27257
                },
                {
                    "node": "2.2.4",
                    "distance": 27257
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "2.6": [
                {
                    "node": "1.1.1",
                    "distance": 33670
                },
                {
                    "node": "1.1.2",
                    "distance": 33670
                },
                {
                    "node": "1.1.3",
                    "distance": 33670
                },
                {
                    "node": "1.1.4",
                    "distance": 33670
                },
                {
                    "node": "1.2.1",
                    "distance": 27257
                },
                {
                    "node": "1.2.2",
                    "distance": 27257
                },
                {
                    "node": "1.2.3",
                    "distance": 27257
                },
                {
                    "node": "1.2.4",
                    "distance": 27257
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 33670
                },
                {
                    "node": "2.1.2",
                    "distance": 33670
                },
                {
                    "node": "2.1.3",
                    "distance": 33670
                },
                {
                    "node": "2.1.4",
                    "distance": 33670
                },
                {
                    "node": "2.2.1",
                    "distance": 27257
                },
                {
                    "node": "2.2.2",
                    "distance": 27257
                },
                {
                    "node": "2.2.3",
                    "distance": 27257
                },
                {
                    "node": "2.2.4",
                    "distance": 27257
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "3.1": [
                {
                    "node": "1.1.1",
                    "distance": 33670
                },
                {
                    "node": "1.1.2",
                    "distance": 33670
                },
                {
                    "node": "1.1.3",
                    "distance": 33670
                },
                {
                    "node": "1.1.4",
                    "distance": 33670
                },
                {
                    "node": "1.2.1",
                    "distance": 27257
                },
                {
                    "node": "1.2.2",
                    "distance": 27257
                },
                {
                    "node": "1.2.3",
                    "distance": 27257
                },
                {
                    "node": "1.2.4",
                    "distance": 27257
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 33670
                },
                {
                    "node": "2.1.2",
                    "distance": 33670
                },
                {
                    "node": "2.1.3",
                    "distance": 33670
                },
                {
                    "node": "2.1.4",
                    "distance": 33670
                },
                {
                    "node": "2.2.1",
                    "distance": 27257
                },
                {
                    "node": "2.2.2",
                    "distance": 27257
                },
                {
                    "node": "2.2.3",
                    "distance": 27257
                },
                {
                    "node": "2.2.4",
                    "distance": 27257
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "3.2": [
                {
                    "node": "1.1.1",
                    "distance": 33670
                },
                {
                    "node": "1.1.2",
                    "distance": 33670
                },
                {
                    "node": "1.1.3",
                    "distance": 33670
                },
                {
                    "node": "1.1.4",
                    "distance": 33670
                },
                {
                    "node": "1.2.1",
                    "distance": 27257
                },
                {
                    "node": "1.2.2",
                    "distance": 27257
                },
                {
                    "node": "1.2.3",
                    "distance": 27257
                },
                {
                    "node": "1.2.4",
                    "distance": 27257
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 33670
                },
                {
                    "node": "2.1.2",
                    "distance": 33670
                },
                {
                    "node": "2.1.3",
                    "distance": 33670
                },
                {
                    "node": "2.1.4",
                    "distance": 33670
                },
                {
                    "node": "2.2.1",
                    "distance": 27257
                },
                {
                    "node": "2.2.2",
                    "distance": 27257
                },
                {
                    "node": "2.2.3",
                    "distance": 27257
                },
                {
                    "node": "2.2.4",
                    "distance": 27257
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "3.3": [
                {
                    "node": "1.1.1",
                    "distance": 33670
                },
                {
                    "node": "1.1.2",
                    "distance": 33670
                },
                {
                    "node": "1.1.3",
                    "distance": 33670
                },
                {
                    "node": "1.1.4",
                    "distance": 33670
                },
                {
                    "node": "1.2.1",
                    "distance": 27257
                },
                {
                    "node": "1.2.2",
                    "distance": 27257
                },
                {
                    "node": "1.2.3",
                    "distance": 27257
                },
                {
                    "node": "1.2.4",
                    "distance": 27257
                },
                {
                    "node": "1.3.1",
                    "distance": 22876
                },
                {
                    "node": "1.3.2",
                    "distance": 22876
                },
                {
                    "node": "1.3.3",
                    "distance": 22876
                },
                {
                    "node": "1.3.4",
                    "distance": 22876
                },
                {
                    "node": "1.4.1",
                    "distance": 19704
                },
                {
                    "node": "1.4.2",
                    "distance": 19704
                },
                {
                    "node": "1.4.3",
                    "distance": 19704
                },
                {
                    "node": "1.4.4",
                    "distance": 19704
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 33670
                },
                {
                    "node": "2.1.2",
                    "distance": 33670
                },
                {
                    "node": "2.1.3",
                    "distance": 33670
                },
                {
                    "node": "2.1.4",
                    "distance": 33670
                },
                {
                    "node": "2.2.1",
                    "distance": 27257
                },
                {
                    "node": "2.2.2",
                    "distance": 27257
                },
                {
                    "node": "2.2.3",
                    "distance": 27257
                },
                {
                    "node": "2.2.4",
                    "distance": 27257
                },
                {
                    "node": "2.3.1",
                    "distance": 22588
                },
                {
                    "node": "2.3.2",
                    "distance": 22588
                },
                {
                    "node": "2.3.3",
                    "distance": 22588
                },
                {
                    "node": "2.3.4",
                    "distance": 22588
                },
                {
                    "node": "2.4.1",
                    "distance": 19416
                },
                {
                    "node": "2.4.2",
                    "distance": 19416
                },
                {
                    "node": "2.4.3",
                    "distance": 19416
                },
                {
                    "node": "2.4.4",
                    "distance": 19416
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "3.4": [
                {
                    "node": "1.1.1",
                    "distance": 40110
                },
                {
                    "node": "1.1.2",
                    "distance": 40110
                },
                {
                    "node": "1.1.3",
                    "distance": 40110
                },
                {
                    "node": "1.1.4",
                    "distance": 40110
                },
                {
                    "node": "1.2.1",
                    "distance": 33628
                },
                {
                    "node": "1.2.2",
                    "distance": 33628
                },
                {
                    "node": "1.2.3",
                    "distance": 33628
                },
                {
                    "node": "1.2.4",
                    "distance": 33628
                },
                {
                    "node": "1.3.1",
                    "distance": 27230
                },
                {
                    "node": "1.3.2",
                    "distance": 27230
                },
                {
                    "node": "1.3.3",
                    "distance": 27230
                },
                {
                    "node": "1.3.4",
                    "distance": 27230
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 40110
                },
                {
                    "node": "2.1.2",
                    "distance": 40110
                },
                {
                    "node": "2.1.3",
                    "distance": 40110
                },
                {
                    "node": "2.1.4",
                    "distance": 40110
                },
                {
                    "node": "2.2.1",
                    "distance": 33628
                },
                {
                    "node": "2.2.2",
                    "distance": 33628
                },
                {
                    "node": "2.2.3",
                    "distance": 33628
                },
                {
                    "node": "2.2.4",
                    "distance": 33628
                },
                {
                    "node": "2.3.1",
                    "distance": 27230
                },
                {
                    "node": "2.3.2",
                    "distance": 27230
                },
                {
                    "node": "2.3.3",
                    "distance": 27230
                },
                {
                    "node": "2.3.4",
                    "distance": 27230
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "3.5": [
                {
                    "node": "1.1.1",
                    "distance": 40110
                },
                {
                    "node": "1.1.2",
                    "distance": 40110
                },
                {
                    "node": "1.1.3",
                    "distance": 40110
                },
                {
                    "node": "1.1.4",
                    "distance": 40110
                },
                {
                    "node": "1.2.1",
                    "distance": 33628
                },
                {
                    "node": "1.2.2",
                    "distance": 33628
                },
                {
                    "node": "1.2.3",
                    "distance": 33628
                },
                {
                    "node": "1.2.4",
                    "distance": 33628
                },
                {
                    "node": "1.3.1",
                    "distance": 27230
                },
                {
                    "node": "1.3.2",
                    "distance": 27230
                },
                {
                    "node": "1.3.3",
                    "distance": 27230
                },
                {
                    "node": "1.3.4",
                    "distance": 27230
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 40110
                },
                {
                    "node": "2.1.2",
                    "distance": 40110
                },
                {
                    "node": "2.1.3",
                    "distance": 40110
                },
                {
                    "node": "2.1.4",
                    "distance": 40110
                },
                {
                    "node": "2.2.1",
                    "distance": 33628
                },
                {
                    "node": "2.2.2",
                    "distance": 33628
                },
                {
                    "node": "2.2.3",
                    "distance": 33628
                },
                {
                    "node": "2.2.4",
                    "distance": 33628
                },
                {
                    "node": "2.3.1",
                    "distance": 27230
                },
                {
                    "node": "2.3.2",
                    "distance": 27230
                },
                {
                    "node": "2.3.3",
                    "distance": 27230
                },
                {
                    "node": "2.3.4",
                    "distance": 27230
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "3.6": [
                {
                    "node": "1.1.1",
                    "distance": 40110
                },
                {
                    "node": "1.1.2",
                    "distance": 40110
                },
                {
                    "node": "1.1.3",
                    "distance": 40110
                },
                {
                    "node": "1.1.4",
                    "distance": 40110
                },
                {
                    "node": "1.2.1",
                    "distance": 33628
                },
                {
                    "node": "1.2.2",
                    "distance": 33628
                },
                {
                    "node": "1.2.3",
                    "distance": 33628
                },
                {
                    "node": "1.2.4",
                    "distance": 33628
                },
                {
                    "node": "1.3.1",
                    "distance": 27230
                },
                {
                    "node": "1.3.2",
                    "distance": 27230
                },
                {
                    "node": "1.3.3",
                    "distance": 27230
                },
                {
                    "node": "1.3.4",
                    "distance": 27230
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 40110
                },
                {
                    "node": "2.1.2",
                    "distance": 40110
                },
                {
                    "node": "2.1.3",
                    "distance": 40110
                },
                {
                    "node": "2.1.4",
                    "distance": 40110
                },
                {
                    "node": "2.2.1",
                    "distance": 33628
                },
                {
                    "node": "2.2.2",
                    "distance": 33628
                },
                {
                    "node": "2.2.3",
                    "distance": 33628
                },
                {
                    "node": "2.2.4",
                    "distance": 33628
                },
                {
                    "node": "2.3.1",
                    "distance": 27230
                },
                {
                    "node": "2.3.2",
                    "distance": 27230
                },
                {
                    "node": "2.3.3",
                    "distance": 27230
                },
                {
                    "node": "2.3.4",
                    "distance": 27230
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "4.1": [
                {
                    "node": "1.1.1",
                    "distance": 40110
                },
                {
                    "node": "1.1.2",
                    "distance": 40110
                },
                {
                    "node": "1.1.3",
                    "distance": 40110
                },
                {
                    "node": "1.1.4",
                    "distance": 40110
                },
                {
                    "node": "1.2.1",
                    "distance": 33628
                },
                {
                    "node": "1.2.2",
                    "distance": 33628
                },
                {
                    "node": "1.2.3",
                    "distance": 33628
                },
                {
                    "node": "1.2.4",
                    "distance": 33628
                },
                {
                    "node": "1.3.1",
                    "distance": 27230
                },
                {
                    "node": "1.3.2",
                    "distance": 27230
                },
                {
                    "node": "1.3.3",
                    "distance": 27230
                },
                {
                    "node": "1.3.4",
                    "distance": 27230
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 40110
                },
                {
                    "node": "2.1.2",
                    "distance": 40110
                },
                {
                    "node": "2.1.3",
                    "distance": 40110
                },
                {
                    "node": "2.1.4",
                    "distance": 40110
                },
                {
                    "node": "2.2.1",
                    "distance": 33628
                },
                {
                    "node": "2.2.2",
                    "distance": 33628
                },
                {
                    "node": "2.2.3",
                    "distance": 33628
                },
                {
                    "node": "2.2.4",
                    "distance": 33628
                },
                {
                    "node": "2.3.1",
                    "distance": 27230
                },
                {
                    "node": "2.3.2",
                    "distance": 27230
                },
                {
                    "node": "2.3.3",
                    "distance": 27230
                },
                {
                    "node": "2.3.4",
                    "distance": 27230
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "4.2": [
                {
                    "node": "1.1.1",
                    "distance": 40110
                },
                {
                    "node": "1.1.2",
                    "distance": 40110
                },
                {
                    "node": "1.1.3",
                    "distance": 40110
                },
                {
                    "node": "1.1.4",
                    "distance": 40110
                },
                {
                    "node": "1.2.1",
                    "distance": 33628
                },
                {
                    "node": "1.2.2",
                    "distance": 33628
                },
                {
                    "node": "1.2.3",
                    "distance": 33628
                },
                {
                    "node": "1.2.4",
                    "distance": 33628
                },
                {
                    "node": "1.3.1",
                    "distance": 27230
                },
                {
                    "node": "1.3.2",
                    "distance": 27230
                },
                {
                    "node": "1.3.3",
                    "distance": 27230
                },
                {
                    "node": "1.3.4",
                    "distance": 27230
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 40110
                },
                {
                    "node": "2.1.2",
                    "distance": 40110
                },
                {
                    "node": "2.1.3",
                    "distance": 40110
                },
                {
                    "node": "2.1.4",
                    "distance": 40110
                },
                {
                    "node": "2.2.1",
                    "distance": 33628
                },
                {
                    "node": "2.2.2",
                    "distance": 33628
                },
                {
                    "node": "2.2.3",
                    "distance": 33628
                },
                {
                    "node": "2.2.4",
                    "distance": 33628
                },
                {
                    "node": "2.3.1",
                    "distance": 27230
                },
                {
                    "node": "2.3.2",
                    "distance": 27230
                },
                {
                    "node": "2.3.3",
                    "distance": 27230
                },
                {
                    "node": "2.3.4",
                    "distance": 27230
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "4.3": [
                {
                    "node": "1.1.1",
                    "distance": 40110
                },
                {
                    "node": "1.1.2",
                    "distance": 40110
                },
                {
                    "node": "1.1.3",
                    "distance": 40110
                },
                {
                    "node": "1.1.4",
                    "distance": 40110
                },
                {
                    "node": "1.2.1",
                    "distance": 33628
                },
                {
                    "node": "1.2.2",
                    "distance": 33628
                },
                {
                    "node": "1.2.3",
                    "distance": 33628
                },
                {
                    "node": "1.2.4",
                    "distance": 33628
                },
                {
                    "node": "1.3.1",
                    "distance": 27230
                },
                {
                    "node": "1.3.2",
                    "distance": 27230
                },
                {
                    "node": "1.3.3",
                    "distance": 27230
                },
                {
                    "node": "1.3.4",
                    "distance": 27230
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 40110
                },
                {
                    "node": "2.1.2",
                    "distance": 40110
                },
                {
                    "node": "2.1.3",
                    "distance": 40110
                },
                {
                    "node": "2.1.4",
                    "distance": 40110
                },
                {
                    "node": "2.2.1",
                    "distance": 33628
                },
                {
                    "node": "2.2.2",
                    "distance": 33628
                },
                {
                    "node": "2.2.3",
                    "distance": 33628
                },
                {
                    "node": "2.2.4",
                    "distance": 33628
                },
                {
                    "node": "2.3.1",
                    "distance": 27230
                },
                {
                    "node": "2.3.2",
                    "distance": 27230
                },
                {
                    "node": "2.3.3",
                    "distance": 27230
                },
                {
                    "node": "2.3.4",
                    "distance": 27230
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "4.4": [
                {
                    "node": "1.1.1",
                    "distance": 40110
                },
                {
                    "node": "1.1.2",
                    "distance": 40110
                },
                {
                    "node": "1.1.3",
                    "distance": 40110
                },
                {
                    "node": "1.1.4",
                    "distance": 40110
                },
                {
                    "node": "1.2.1",
                    "distance": 33628
                },
                {
                    "node": "1.2.2",
                    "distance": 33628
                },
                {
                    "node": "1.2.3",
                    "distance": 33628
                },
                {
                    "node": "1.2.4",
                    "distance": 33628
                },
                {
                    "node": "1.3.1",
                    "distance": 27230
                },
                {
                    "node": "1.3.2",
                    "distance": 27230
                },
                {
                    "node": "1.3.3",
                    "distance": 27230
                },
                {
                    "node": "1.3.4",
                    "distance": 27230
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 40110
                },
                {
                    "node": "2.1.2",
                    "distance": 40110
                },
                {
                    "node": "2.1.3",
                    "distance": 40110
                },
                {
                    "node": "2.1.4",
                    "distance": 40110
                },
                {
                    "node": "2.2.1",
                    "distance": 33628
                },
                {
                    "node": "2.2.2",
                    "distance": 33628
                },
                {
                    "node": "2.2.3",
                    "distance": 33628
                },
                {
                    "node": "2.2.4",
                    "distance": 33628
                },
                {
                    "node": "2.3.1",
                    "distance": 27230
                },
                {
                    "node": "2.3.2",
                    "distance": 27230
                },
                {
                    "node": "2.3.3",
                    "distance": 27230
                },
                {
                    "node": "2.3.4",
                    "distance": 27230
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "4.5": [
                {
                    "node": "1.1.1",
                    "distance": 40110
                },
                {
                    "node": "1.1.2",
                    "distance": 40110
                },
                {
                    "node": "1.1.3",
                    "distance": 40110
                },
                {
                    "node": "1.1.4",
                    "distance": 40110
                },
                {
                    "node": "1.2.1",
                    "distance": 33628
                },
                {
                    "node": "1.2.2",
                    "distance": 33628
                },
                {
                    "node": "1.2.3",
                    "distance": 33628
                },
                {
                    "node": "1.2.4",
                    "distance": 33628
                },
                {
                    "node": "1.3.1",
                    "distance": 27230
                },
                {
                    "node": "1.3.2",
                    "distance": 27230
                },
                {
                    "node": "1.3.3",
                    "distance": 27230
                },
                {
                    "node": "1.3.4",
                    "distance": 27230
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 40110
                },
                {
                    "node": "2.1.2",
                    "distance": 40110
                },
                {
                    "node": "2.1.3",
                    "distance": 40110
                },
                {
                    "node": "2.1.4",
                    "distance": 40110
                },
                {
                    "node": "2.2.1",
                    "distance": 33628
                },
                {
                    "node": "2.2.2",
                    "distance": 33628
                },
                {
                    "node": "2.2.3",
                    "distance": 33628
                },
                {
                    "node": "2.2.4",
                    "distance": 33628
                },
                {
                    "node": "2.3.1",
                    "distance": 27230
                },
                {
                    "node": "2.3.2",
                    "distance": 27230
                },
                {
                    "node": "2.3.3",
                    "distance": 27230
                },
                {
                    "node": "2.3.4",
                    "distance": 27230
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        },
        {
            "4.6": [
                {
                    "node": "1.1.1",
                    "distance": 40110
                },
                {
                    "node": "1.1.2",
                    "distance": 40110
                },
                {
                    "node": "1.1.3",
                    "distance": 40110
                },
                {
                    "node": "1.1.4",
                    "distance": 40110
                },
                {
                    "node": "1.2.1",
                    "distance": 33628
                },
                {
                    "node": "1.2.2",
                    "distance": 33628
                },
                {
                    "node": "1.2.3",
                    "distance": 33628
                },
                {
                    "node": "1.2.4",
                    "distance": 33628
                },
                {
                    "node": "1.3.1",
                    "distance": 27230
                },
                {
                    "node": "1.3.2",
                    "distance": 27230
                },
                {
                    "node": "1.3.3",
                    "distance": 27230
                },
                {
                    "node": "1.3.4",
                    "distance": 27230
                },
                {
                    "node": "1.4.1",
                    "distance": 20886
                },
                {
                    "node": "1.4.2",
                    "distance": 20886
                },
                {
                    "node": "1.4.3",
                    "distance": 20886
                },
                {
                    "node": "1.4.4",
                    "distance": 20886
                },
                {
                    "node": "1.5.1",
                    "distance": 18522
                },
                {
                    "node": "1.5.2",
                    "distance": 18522
                },
                {
                    "node": "1.5.3",
                    "distance": 18522
                },
                {
                    "node": "1.5.4",
                    "distance": 18522
                },
                {
                    "node": "1.6.1",
                    "distance": 18522
                },
                {
                    "node": "1.6.2",
                    "distance": 18522
                },
                {
                    "node": "1.6.3",
                    "distance": 18522
                },
                {
                    "node": "1.6.4",
                    "distance": 18522
                },
                {
                    "node": "1.7.1",
                    "distance": 18522
                },
                {
                    "node": "1.7.2",
                    "distance": 18522
                },
                {
                    "node": "1.7.3",
                    "distance": 18522
                },
                {
                    "node": "1.7.4",
                    "distance": 18522
                },
                {
                    "node": "2.1.1",
                    "distance": 40110
                },
                {
                    "node": "2.1.2",
                    "distance": 40110
                },
                {
                    "node": "2.1.3",
                    "distance": 40110
                },
                {
                    "node": "2.1.4",
                    "distance": 40110
                },
                {
                    "node": "2.2.1",
                    "distance": 33628
                },
                {
                    "node": "2.2.2",
                    "distance": 33628
                },
                {
                    "node": "2.2.3",
                    "distance": 33628
                },
                {
                    "node": "2.2.4",
                    "distance": 33628
                },
                {
                    "node": "2.3.1",
                    "distance": 27230
                },
                {
                    "node": "2.3.2",
                    "distance": 27230
                },
                {
                    "node": "2.3.3",
                    "distance": 27230
                },
                {
                    "node": "2.3.4",
                    "distance": 27230
                },
                {
                    "node": "2.4.1",
                    "distance": 20886
                },
                {
                    "node": "2.4.2",
                    "distance": 20886
                },
                {
                    "node": "2.4.3",
                    "distance": 20886
                },
                {
                    "node": "2.4.4",
                    "distance": 20886
                },
                {
                    "node": "2.5.1",
                    "distance": 17946
                },
                {
                    "node": "2.5.2",
                    "distance": 17946
                },
                {
                    "node": "2.5.3",
                    "distance": 17946
                },
                {
                    "node": "2.5.4",
                    "distance": 17946
                },
                {
                    "node": "2.6.1",
                    "distance": 17946
                },
                {
                    "node": "2.6.2",
                    "distance": 17946
                },
                {
                    "node": "2.6.3",
                    "distance": 17946
                },
                {
                    "node": "2.6.4",
                    "distance": 17946
                },
                {
                    "node": "2.7.1",
                    "distance": 17946
                },
                {
                    "node": "2.7.2",
                    "distance": 17946
                },
                {
                    "node": "2.7.3",
                    "distance": 17946
                },
                {
                    "node": "2.7.4",
                    "distance": 17946
                }
            ]
        }
    ]
}


# extra distances for each component type
component_extra_distances = {
    "Component_1": 500,
    "Component_2": 500,
    "Component_3": 800,
    "Component_4": 2000,
    "Component_5": 1500,
    "Component_7": 500,
    "Component_9": 2500,
    "Component_10": 1000,
    "Component_11": 1000,
    "Component_12": 500,
    "Component_13": 500,
    "Component_14": 500,
    "Component_15": 800,
    "Component_16": 800,
}

def filter_distance_matrix_with_e_constraint(matrix, random_config, extra_distances):
    filtered_matrix = {"0.0": []}

    containers = random_config["containers"]
    kit_holders = random_config["kit_holders"]

    for kh_key, kh_value in kit_holders.items():
        kh_position = kh_value["kh_position"]  # e.g., "1"

        for kh_content in kh_value["contents"]:
            kit_position = kh_content["position"]  # e.g., "1.1"
            kit_component = kh_content["type"]  # e.g., "Component_5"

            valid_nodes = []

            for container_key, container_value in containers.items():
                for cont_content in container_value["contents"]:
                    cont_position = cont_content["position"]  # e.g., "1.5.1"
                    cont_component = cont_content["type"]  # e.g., "Component_5"

                    if kit_component == cont_component:
                        distance = get_distance_from_matrix(matrix, kit_position, cont_position)
                        if distance is not None:
                            # add extra distance
                            adjusted_distance = distance + extra_distances.get(kit_component, 0)
                            valid_nodes.append({"node": cont_position, "distance": adjusted_distance})

            unique_nodes = list({node["node"]: node for node in valid_nodes}.values())

            if unique_nodes:
                filtered_matrix["0.0"].append({
                    kit_position: unique_nodes
                })

    return filtered_matrix


def get_distance_from_matrix(matrix, kh_position, container_position):
    """
    Retrieve the distance between a kit holder position and a container position from the matrix.
    """
    for kh_entry in matrix.get("0.0", []):
        if kh_position in kh_entry:
            for container in kh_entry[kh_position]:
                if container["node"] == container_position:
                    return container["distance"]
    return None


filtered_matrix = filter_distance_matrix_with_e_constraint(distance_matrix, random_config, component_extra_distances)


with open("random_configuration_distance_matrix_with_extra_distance.json", "w") as f:
    json.dump(filtered_matrix, f, indent=4)

print("Filtered distance matrix with e constraint saved successfully.")

