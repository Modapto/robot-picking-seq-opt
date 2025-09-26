import copy

def generate_kh_configuration(kh_setup, kit_holders_template):
    configured_kh = {}
    for idx, kh_id in enumerate(kh_setup, start=1):
        if kh_id == "EMPTY":
            continue
        if kh_id in kit_holders_template:
            kh_data = copy.deepcopy(kit_holders_template[kh_id])
            for i, content in enumerate(kh_data["contents"], start=1):
                content["position"] = f"{idx}.{i}"
            configured_kh[f"KH{idx}"] = {
                "kh_position": str(idx),
                "contents": kh_data["contents"]
            }
        else:
            configured_kh[f"KH{idx}"] = {"kh_position": kh_id, "contents": []}
    return configured_kh

def filter_distance_matrix(matrix, random_config):
    filtered_matrix = []
    containers = random_config["containers"]
    kit_holders = random_config["kit_holders"]

    # Transform distance matrix to a lookup dictionary (robust against spacing)
    matrix_dict = {}
    for entry in matrix:
        edge_str = entry["edge"].strip("()")
        source, target = [x.strip() for x in edge_str.split(",")]
        if source not in matrix_dict:
            matrix_dict[source] = {}
        matrix_dict[source][target] = entry["distance"]

    # Track active KH positions for later filtering
    kh_positions = []
    for kh_data in kit_holders.values():
        for content in kh_data["contents"]:
            kh_positions.append(content["position"])
    print(f"✅ Active KH Positions: {kh_positions}")

    # Add edges: 0.0 → all gravity racks
    if "0.0" in matrix_dict:
        for target, distance in matrix_dict["0.0"].items():
            filtered_matrix.append({"edge": f"(0.0, {target})", "distance": distance + 2000})

    # Add edge: 0.0.0 → 0.0
    if "0.0.0" in matrix_dict and "0.0" in matrix_dict["0.0.0"]:
        filtered_matrix.append({"edge": "(0.0.0, 0.0)", "distance": matrix_dict["0.0.0"]["0.0"]})

    # Add edges: KH → 0.0.0
    for pos in kh_positions:
        if pos in matrix_dict and "0.0.0" in matrix_dict[pos]:
            filtered_matrix.append({"edge": f"({pos}, 0.0.0)", "distance": matrix_dict[pos]["0.0.0"] + 2000})

    # Add edges: GR → KH (component-based)
    for container in containers.values():
        for gr_content in container["contents"]:
            for kh_data in kit_holders.values():
                for kh_content in kh_data["contents"]:
                    if kh_content["type"] == gr_content["type"]:
                        source = gr_content["position"]
                        target = kh_content["position"]
                        if source in matrix_dict and target in matrix_dict[source]:
                            filtered_matrix.append({
                                "edge": f"({source}, {target})",
                                "distance": matrix_dict[source][target] + 2000
                            })

    # Add edges: KH → GR
    for kh_data in kit_holders.values():
        for kh_content in kh_data["contents"]:
            source = kh_content["position"]
            if source in matrix_dict:
                for target, distance in matrix_dict[source].items():
                    if target.startswith("1.") or target.startswith("2."):
                        filtered_matrix.append({
                            "edge": f"({source}, {target})",
                            "distance": distance + 2000
                        })

    # Add edges: GR → GR
    for gr_a in containers.values():
        for content_a in gr_a["contents"]:
            pos_a = content_a["position"]
            if pos_a in matrix_dict:
                for gr_b in containers.values():
                    for content_b in gr_b["contents"]:
                        pos_b = content_b["position"]
                        if pos_a != pos_b and pos_b in matrix_dict[pos_a]:
                            filtered_matrix.append({
                                "edge": f"({pos_a}, {pos_b})",
                                "distance": matrix_dict[pos_a][pos_b] + 2000
                            })

    # Add edges: KH → KH (only among active KH positions)
    for kh1 in kh_positions:
        for kh2 in kh_positions:
            if kh1 == kh2:
                continue
            distance = matrix_dict.get(kh1, {}).get(kh2)
            if distance is None:
                distance = matrix_dict.get(kh2, {}).get(kh1)
            if distance is not None and distance < 1000000:
                filtered_matrix.append({
                    "edge": f"({kh1}, {kh2})",
                    "distance": distance + 2000
                })

    return filtered_matrix
