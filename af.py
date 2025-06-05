
import json
# def extract_kh_gr_nodes(input_json):
#     kh_sequences = input_json["data"]["kh_sequences"]
#     kit_holders_template = input_json["data"]["kit_holders_template"]
#     gr_sequence = input_json["data"]["gr_sequence"]
#     containers_template = input_json["data"]["containers_template"]
#
#     kh_nodes = {}
#     gr_nodes = {}
#
#     # Extract KH nodes
#     for pos_dict in kh_sequences:
#         for kh_pos, kh_type in pos_dict.items():
#             if kh_type not in kit_holders_template:
#                 print(f"[WARNING] Unknown KH type {kh_type} in KH position {kh_pos}")
#                 continue
#             for item in kit_holders_template[kh_type]["contents"]:
#                 kh_node = f"{kh_pos}.{item['position']}"
#                 kh_nodes[kh_node] = item["type"]
#
#     # Extract GR nodes
#     for pos_dict in gr_sequence:
#         for gr_pos, container_type in pos_dict.items():
#             if container_type not in containers_template:
#                 print(f"[WARNING] Unknown Container type {container_type} in GR position {gr_pos}")
#                 continue
#             for item in containers_template[container_type]["contents"]:
#                 gr_node = f"{gr_pos}.{item['position']}"
#                 gr_nodes[gr_node] = item["type"]
#
#     return kh_nodes, gr_nodes
#
with open("new_input.json") as f:
    input_data = json.load(f)

# # Run the extractor
# kh_nodes, gr_nodes = extract_kh_gr_nodes(input_data)

# # Print a few samples to verify
# print("Sample KH nodes:")
# for k, v in list(kh_nodes.items())[:5]:
#     print(f"{k} -> {v}")
#
# print("\nSample GR nodes:")
# for k, v in list(gr_nodes.items())[:5]:
#     print(f"{k} -> {v}")

# Step 1: Load the full distance matrix from your input JSON
raw_matrix = input_data["data"]["distance_matrix"]

# # Step 2: Convert it to a lookup dictionary: "source->target" -> distance
# full_matrix = {}
# for entry in raw_matrix:
#     edge = entry["edge"].strip("()").replace(" ", "").split(",")
#     src, dst = edge[0], edge[1]
#     full_matrix[f"{src}->{dst}"] = entry["distance"]



# def generate_filtered_distance_matrix(raw_distance_matrix, container_types, kit_holder_types, kh_sequences, gr_sequence):
#     # Step 1: Map KH nodes to their component types
#     kh_nodes = {}
#     for entry in kh_sequences:
#         for kh_pos, kh_id in entry.items():
#             if kh_id in kit_holder_types:
#                 for comp in kit_holder_types[kh_id]["contents"]:
#                     if isinstance(comp, dict):
#                         position = comp["position"]
#                         comp_type = comp["type"]
#                         kh_node = f"{kh_pos}.{position}"
#                         kh_nodes[kh_node] = comp_type
#
#     # Step 2: Map GR nodes to their component types
#     gr_nodes = {}
#     for entry in gr_sequence:
#         for gr_pos, container_id in entry.items():
#             if container_id in container_types:
#                 contents = container_types[container_id].get("contents", [])
#                 for comp in contents:
#                     if isinstance(comp, dict) and "position" in comp and "type" in comp:
#                         position = comp["position"]
#                         comp_type = comp["type"]
#                         gr_node = f"{gr_pos}.{position}"
#                         gr_nodes[gr_node] = comp_type
#                     else:
#                         print(f"⚠️ Unexpected format in container {container_id}: {comp}")
#
#     # Step 3: Convert raw distance matrix to lookup dict
#     distance_lookup = {}
#     for entry in raw_distance_matrix:
#         edge_str = entry["edge"].strip("()")
#         src, dst = edge_str.split(", ")
#         src = src.strip("'")
#         dst = dst.strip("'")
#         distance_lookup[(src, dst)] = entry["distance"]
#
#     # Step 4: Generate filtered edges
#     filtered = []
#
#     # 0.0 → all GR nodes
#     for gr_node in gr_nodes:
#         key = ("0.0", gr_node)
#         if key in distance_lookup:
#             filtered.append({"edge": f"({key[0]}, {key[1]})", "distance": distance_lookup[key]})
#
#     # GR → KH (only if component type matches)
#     for gr_node, gr_type in gr_nodes.items():
#         for kh_node, kh_type in kh_nodes.items():
#             if gr_type == kh_type:
#                 key = (gr_node, kh_node)
#                 if key in distance_lookup:
#                     filtered.append({"edge": f"({key[0]}, {key[1]})", "distance": distance_lookup[key]})
#
#     # KH → 0.0.0
#     for kh_node in kh_nodes:
#         key = (kh_node, "0.0.0")
#         if key in distance_lookup:
#             filtered.append({"edge": f"({key[0]}, 0.0.0)", "distance": distance_lookup[key]})
#
#     # Final 0.0.0 → 0.0 edge
#     if ("0.0.0", "0.0") in distance_lookup:
#         filtered.append({"edge": "(0.0.0, 0.0)", "distance": distance_lookup[("0.0.0", "0.0")]})
#
#     # Debugging output
#     print("Sample KH nodes:")
#     for k, v in list(kh_nodes.items())[:20]:
#         print(f"{k} -> {v}")
#
#     print("\nSample GR nodes:")
#     for k, v in list(gr_nodes.items())[:5]:
#         print(f"{k} -> {v}")
#
#     print(f"\nFiltered edge count: {len(filtered)}")
#     print("Filtered edges:")
#     for edge in filtered[:200]:
#         print(edge)
#
#     return filtered

def generate_kh_nodes(kh_sequences, kit_holder_types):
    kh_nodes = {}
    for entry in kh_sequences:
        for kh_pos, kh_id in entry.items():
            if kh_id in kit_holder_types:
                for comp in kit_holder_types[kh_id].get("contents", []):
                    if isinstance(comp, dict):
                        position = comp["position"]
                        comp_type = comp["type"]
                        kh_node = f"{kh_pos}.{position}"
                        kh_nodes[kh_node] = comp_type
    return kh_nodes

def generate_gr_nodes(gr_sequence, container_types):
    gr_nodes = {}
    for entry in gr_sequence:
        for gr_pos, container_id in entry.items():
            if container_id in container_types:
                contents = container_types[container_id].get("contents", [])
                for comp in contents:
                    if isinstance(comp, dict) and "position" in comp and "type" in comp:
                        position = comp["position"]
                        comp_type = comp["type"]
                        gr_node = f"{gr_pos}.{position}"
                        gr_nodes[gr_node] = comp_type
    return gr_nodes

def extend_distance_matrix(gr_nodes, kh_nodes, original_matrix, fallback_distance=99999):
    extended = []

    # Step 1: Build lookup
    original_lookup = {
        tuple(e["edge"].strip("()").replace("'", "").split(", ")): e["distance"]
        for e in original_matrix
    }

    # Step 2: Add 0.0 → GR edges
    for gr_node in gr_nodes:
        key = ("0.0", gr_node)
        distance = original_lookup.get(key, fallback_distance)
        extended.append({"edge": f"({key[0]}, {key[1]})", "distance": distance})

    # Step 3: Add GR → KH edges if types match
    for gr_node, gr_type in gr_nodes.items():
        for kh_node, kh_type in kh_nodes.items():
            if gr_type == kh_type:
                key = (gr_node, kh_node)
                distance = original_lookup.get(key, fallback_distance)
                extended.append({"edge": f"({key[0]}, {key[1]})", "distance": distance})

    # Step 4: Add KH → 0.0.0
    for kh_node in kh_nodes:
        key = (kh_node, "0.0.0")
        distance = original_lookup.get(key, fallback_distance)
        extended.append({"edge": f"({key[0]}, {key[1]})", "distance": distance})

    # Step 5: Add 0.0.0 → 0.0 if exists
    key = ("0.0.0", "0.0")
    distance = original_lookup.get(key, fallback_distance)
    extended.append({"edge": f"({key[0]}, {key[1]})", "distance": distance})

    return extended

def generate_filtered_distance_matrix(extended_matrix, gr_nodes, kh_nodes):
    filtered = []

    for entry in extended_matrix:
        edge_str = entry["edge"].strip("()")
        src, dst = edge_str.split(", ")
        src = src.strip()
        dst = dst.strip()

        # 0.0 → GR
        if src == "0.0" and dst in gr_nodes:
            filtered.append(entry)

        # GR → KH (already type-matched during extension)
        elif src in gr_nodes and dst in kh_nodes:
            filtered.append(entry)

        # KH → 0.0.0
        elif src in kh_nodes and dst == "0.0.0":
            filtered.append(entry)

        # 0.0.0 → 0.0
        elif src == "0.0.0" and dst == "0.0":
            filtered.append(entry)

    # Logging
    print("Sample KH nodes:")
    for k, v in list(kh_nodes.items())[:5]:
        print(f"{k} -> {v}")

    print("\nSample GR nodes:")
    for k, v in list(gr_nodes.items())[:5]:
        print(f"{k} -> {v}")

    print(f"\nFiltered edge count: {len(filtered)}")
    print("Filtered edges:")
    for edge in filtered[:200]:
        print(edge)

    return filtered







raw_distance_matrix = input_data["data"]["distance_matrix"]
container_types = input_data["data"]["containers_template"]
kit_holder_types = input_data["data"]["kit_holders_template"]
kh_sequences = input_data["data"]["kh_sequences"]
gr_sequence = input_data["data"]["gr_sequence"]

# filtered = generate_filtered_distance_matrix(
#     raw_distance_matrix,
#     container_types,
#     kit_holder_types,
#     kh_sequences,
#     gr_sequence
# )

# Step 1: Generate node maps
gr_nodes = generate_gr_nodes(gr_sequence, container_types)
kh_nodes = generate_kh_nodes(kh_sequences, kit_holder_types)

# Step 2: Extend the distance matrix
extended_matrix = extend_distance_matrix(gr_nodes, kh_nodes, raw_distance_matrix)

# Step 3: Filter it for optimization logic
filtered_matrix = generate_filtered_distance_matrix(extended_matrix, gr_nodes, kh_nodes)



# print("Filtered edge count:", len(filtered))
# print("Sample edges:", filtered[:10])





# filtered = filter_distance_matrix(raw_matrix, kh_nodes, gr_nodes)
# print("Filtered edges:")
# for edge in filtered[:200]:
#     print(edge)


# # Step 1: Reconstruct the config from input_json
# random_config = reconstruct_config_from_input(input_data)
#
# # Step 2: Filter matrix
# filtered = filter_distance_matrix(full_matrix, random_config)
#
# # Step 3: Preview result
# for edge in filtered[:20]:
#     print(edge)

