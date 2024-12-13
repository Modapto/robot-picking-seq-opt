# Containers dictionary
from scipy.spatial import distance_matrix
#random positioning of containers
containers = {
    "Container_1": {"gr_position": "1.1","contents" : [{"position":"1.1.1","type":"Component_1"},{"position":"1.1.2","type":"Component_1"},{"position":"1.1.3","type":"Component_1"},{"position":"1.1.4","type":"Component_1"}]},
    "Container_2": ["Component_2"],
    "Container_3": ["Component_3"],
    "Container_4": ["Component_4"],
    "Container_5": ["Component_5"],
    "Container_6": ["Component_7"],
    "Container_7": ["Component_9"],
    "Container_8": ["Component_10"],
    "Container_9": ["Component_11"],
    "Container_10": ["Component_12"],
    "Container_11": ["Component_13"],
    "Container_12": ["Component_14"],
    "Container_13": ["Component_15"],
    "Container_14": ["Component_16"]
}
#random selection and positioning of kitholders
# Kit Holders dictionary
kit_holders = {
    "KH001": {"kh_position": "1","contents":[{"position":"1.1","type":"Component_5"}, {"position":"1.2","type":"Component_15"}, {"position":"1.3","type":"Component_3"}, {"position":"1.4","type":"Component_16"}, {"position":"1.5","type":"Component_14"}, {"position":"1.6","type":"Component_11"}]},
    "KH002": ["Component_4", "Component_2", "Component_12", "Component_10"],
    "KH003": ["Component_9", "Component_13", "Component_1", "Component_7", "Component_10"]
}


distance_matrix = {
    "0.0": [
        {
            "1.1": [
                {
                    "node": "1.1.1",
                    "distance": 17654
                },
                {
                    "node": "1.1.2",
                    "distance": 17656
                },
                {
                    "node": "1.1.3",
                    "distance": 17656
                }
            ]
        },
        {
            "1.2": [
                {
                    "node": "1.1.1",
                    "distance": 18765
                },
                {
                    "node": "1.1.2",
                    "distance": 19567
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
