# Containers dictionary
from scipy.spatial import distance_matrix
#random positioning of containers
containers = {
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
    "Container_8": {"gr_position": "1.8", "contents": [{"position": "1.8.1", "type": "Component_10"},
                                                       {"position": "1.8.2", "type": "Component_10"},
                                                       {"position": "1.8.3", "type": "Component_10"},
                                                       {"position": "1.8.4", "type": "Component_10"}]},
    "Container_9": {"gr_position": "1.9", "contents": [{"position": "1.9.1", "type": "Component_11"},
                                                       {"position": "1.9.2", "type": "Component_11"},
                                                       {"position": "1.9.3", "type": "Component_11"},
                                                       {"position": "1.9.4", "type": "Component_11"}]},
    "Container_10": {"gr_position": "1.10", "contents": [{"position": "1.10.1", "type": "Component_12"},
                                                       {"position": "1.10.2", "type": "Component_12"},
                                                       {"position": "1.10.3", "type": "Component_12"},
                                                       {"position": "1.10.4", "type": "Component_12"}]},
    "Container_11": {"gr_position": "1.11", "contents": [{"position": "1.11.1", "type": "Component_13"},
                                                       {"position": "1.11.2", "type": "Component_13"},
                                                       {"position": "1.11.3", "type": "Component_13"},
                                                       {"position": "1.11.4", "type": "Component_13"}]},
    "Container_12": {"gr_position": "1.12", "contents": [{"position": "1.12.1", "type": "Component_14"},
                                                       {"position": "1.12.2", "type": "Component_14"},
                                                       {"position": "1.12.3", "type": "Component_14"},
                                                       {"position": "1.12.4", "type": "Component_14"}]},
    "Container_13": {"gr_position": "1.13", "contents": [{"position": "1.13.1", "type": "Component_15"},
                                                       {"position": "1.13.2", "type": "Component_15"},
                                                       {"position": "1.13.3", "type": "Component_15"},
                                                       {"position": "1.13.4", "type": "Component_15"}]},
    "Container_14": {"gr_position": "1.14", "contents": [{"position": "1.14.1", "type": "Component_16"},
                                                       {"position": "1.14.2", "type": "Component_16"},
                                                       {"position": "1.14.3", "type": "Component_16"},
                                                       {"position": "1.14.4", "type": "Component_16"}]}
}
#random selection and positioning of kitholders
# Kit Holders dictionary
kit_holders = {
    "KH001": {"kh_position": "1",
              "contents": [{"position": "1.1", "type": "Component_5"},
                           {"position": "1.2", "type": "Component_15"},
                           {"position": "1.3", "type": "Component_3"},
                           {"position": "1.4", "type": "Component_16"},
                           {"position": "1.5", "type": "Component_14"},
                           {"position": "1.6", "type": "Component_11"}]},
    "KH002": {"kh_position": "2",
              "contents": [{"position": "2.1", "type": "Component_4"},
                           {"position": "2.2", "type": "Component_2"},
                           {"position": "2.3", "type": "Component_12"},
                           {"position": "2.4", "type": "Component_10"}]},
    "KH003": {"kh_position": "3",
              "contents": [{"position": "3.1", "type": "Component_9"},
                           {"position": "3.2", "type": "Component_13"},
                           {"position": "3.3", "type": "Component_1"},
                           {"position": "3.4", "type": "Component_7"},
                           {"position": "3.5", "type": "Component_10"}]},
    "KH001": {"kh_position": "4",
              "contents": [{"position": "4.1", "type": "Component_5"},
                           {"position": "4.2", "type": "Component_15"},
                           {"position": "4.3", "type": "Component_3"},
                           {"position": "4.4", "type": "Component_16"},
                           {"position": "4.5", "type": "Component_14"},
                           {"position": "4.6", "type": "Component_11"}]},
}


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
                }
            ]
        }
    ]
}



# Function For Connectivity
def connectivity(containers, kit_holders):
    # connectivity dicts
    kitholder_to_containers = {}
    container_to_kitholders = {}

    # map each kit holder to all containers (KH -> All Containers)
    for kitholder in kit_holders:
        kitholder_to_containers[kitholder] = list(containers.keys())

    # map each container to specific kit holders (Container -> Specific KHs)
    for container, components in containers.items():
        container_to_kitholders[container] = []
        for KH, kh_components in kit_holders.items():
            # Check if any component in the container is required by the kit holder
            if any(component in kh_components for component in components):
                container_to_kitholders[container].append(kitholder)

    return kitholder_to_containers, container_to_kitholders

kitholder_to_containers, container_to_kitholders = connectivity(containers, kit_holders)


print("Kit Holder to All Containers:")
for kitholder, connected_containers in kitholder_to_containers.items():
    print(f"{kitholder} -> {', '.join(connected_containers)}")

print("\nContainer to Specific Kit Holders:")
for container, connected_kitholders in container_to_kitholders.items():
    print(f"{container} -> {', '.join(connected_kitholders)}")
