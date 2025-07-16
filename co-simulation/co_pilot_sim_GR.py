import random
import copy

def filter_distance_matrix(matrix, random_config):
    filtered_matrix = []
    containers = random_config["containers"]
    kit_holders = random_config["kit_holders"]

    # Transform distance matrix to a lookup dictionary
    matrix_dict = {}
    for entry in matrix:
        edge = entry["edge"].strip("()").split(", ")
        source, target = edge[0], edge[1]
        if source not in matrix_dict:
            matrix_dict[source] = {}
        matrix_dict[source][target] = entry["distance"]

    # Add edges: 0.0 to all gravity racks
    if "0.0" in matrix_dict:
        for target, distance in matrix_dict["0.0"].items():
            filtered_matrix.append({"edge": f"(0.0, {target})", "distance": distance + 2000})

    # Add edges: 0.0.0 to 0.0
    if "0.0.0" in matrix_dict and "0.0" in matrix_dict["0.0.0"]:
        filtered_matrix.append({"edge": "(0.0.0, 0.0)", "distance": matrix_dict["0.0.0"]["0.0"]})

    # Add edges: Kit holders to 0.0.0
    for kh_key, kh_value in kit_holders.items():
        for kh_content in kh_value["contents"]:
            if kh_content["position"] in matrix_dict and "0.0.0" in matrix_dict[kh_content["position"]]:
                filtered_matrix.append({"edge": f"({kh_content['position']}, 0.0.0)", "distance": matrix_dict[kh_content["position"]]["0.0.0"] + 2000})

    # Add edges: Gravity racks to specific kit holders
    for container_key, container_value in containers.items():
        for cont_content in container_value["contents"]:
            for kh_key, kh_value in kit_holders.items():
                for kh_content in kh_value["contents"]:
                    if kh_content["type"] == cont_content["type"]:
                        if cont_content["position"] in matrix_dict and kh_content["position"] in matrix_dict[cont_content["position"]]:
                            filtered_matrix.append({"edge": f"({cont_content['position']}, {kh_content['position']})",
                                                    "distance": matrix_dict[cont_content["position"]][kh_content["position"]] + 2000})

    # Add edges: Kit holders to all gravity racks
    for kh_key, kh_value in kit_holders.items():
        for kh_content in kh_value["contents"]:
            if kh_content["position"] in matrix_dict:
                for target, distance in matrix_dict[kh_content["position"]].items():
                    if target.startswith("1.") or target.startswith("2."):
                        filtered_matrix.append({"edge": f"({kh_content['position']}, {target})", "distance": distance + 2000})

    return filtered_matrix

def containers_from_gr_sequence(gr_seq, containers_template):
    """
    Turns [{"1.1": "Container_1"}, …] into the classic
    {"Container_1": {"gr_position": "1.1", "contents": …}, …}
    """
    import copy
    cfg = {}
    for mapping in gr_seq:
        pos, cid = next(iter(mapping.items()))
        if cid not in containers_template:
            raise KeyError(f"{cid} absent from containers_template")
        c = copy.deepcopy(containers_template[cid])
        c["gr_position"] = pos
        for i, comp in enumerate(c["contents"], start=1):
            comp["position"] = f"{pos}.{i}"
        cfg[cid] = c
    return cfg

def gr_sequence_from_containers(containers_dict):
    """
    Turn {'Container_1': {'gr_position': '1.1', …}, …}
    →  [ {'1.1': 'Container_1'}, {'1.2': 'Container_2'}, … ]
    Positions are sorted row-major (row.column as ints).
    """
    tmp = [(meta["gr_position"], cid) for cid, meta in containers_dict.items()]

    def sort_key(item):
        row, col = map(int, item[0].split('.'))
        return (row, col)

    return [{pos: cid} for pos, cid in sorted(tmp, key=sort_key)]

def shuffle_container_positions(containers_dict):
    """
    Returns a *new* dict where each container ID keeps its own contents
    but is assigned a random, unique GR position.
    """
    shuffled = copy.deepcopy(containers_dict)

    # Take the existing list of positions (['1.1', '1.2', …, '2.7'])
    positions = [meta["gr_position"] for meta in shuffled.values()]
    random.shuffle(positions)

    for (cid, meta), new_pos in zip(shuffled.items(), positions):
        meta["gr_position"] = new_pos
        # update the four inner slot co-ordinates
        for i, comp in enumerate(meta["contents"], 1):
            comp["position"] = f"{new_pos}.{i}"
    return shuffled
