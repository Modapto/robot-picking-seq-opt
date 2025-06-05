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

    # Step 1: Build original edge lookup
    original_lookup = {
        tuple(e["edge"].strip("()").replace("'", "").split(", ")): e["distance"]
        for e in original_matrix
    }

    # Step 2: Smart fallback helper
    def get_fallback_distance(src, dst):
        # Exact match
        if (src, dst) in original_lookup:
            return original_lookup[(src, dst)]

        def get_base(n):
            parts = n.split(".")
            if len(parts) == 2:
                return parts[0]
            elif len(parts) == 3:
                return ".".join(parts[:2])
            return n

        base_src = get_base(src)
        base_dst = get_base(dst)

        for (s, d), dist in original_lookup.items():
            if get_base(s) == base_src and d == dst:
                return dist
        for (s, d), dist in original_lookup.items():
            if s == src and get_base(d) == base_dst:
                return dist
        for (s, d), dist in original_lookup.items():
            if get_base(s) == base_src and get_base(d) == base_dst:
                return dist

        return fallback_distance

    # Step 3: Add 0.0 → GR edges
    for gr_node in gr_nodes:
        distance = get_fallback_distance("0.0", gr_node)
        extended.append({"edge": f"(0.0, {gr_node})", "distance": distance})

    # Step 4: Add GR → KH edges (if types match)
    for gr_node, gr_type in gr_nodes.items():
        for kh_node, kh_type in kh_nodes.items():
            if gr_type == kh_type:
                distance = get_fallback_distance(gr_node, kh_node)
                extended.append({"edge": f"({gr_node}, {kh_node})", "distance": distance})

    # ✅ Step 5: Add KH → GR edges (ALL combinations, regardless of type)
    for kh_node in kh_nodes:
        for gr_node in gr_nodes:
            distance = get_fallback_distance(kh_node, gr_node)
            extended.append({"edge": f"({kh_node}, {gr_node})", "distance": distance})

    # Step 6: Add KH → 0.0.0 edges
    for kh_node in kh_nodes:
        distance = get_fallback_distance(kh_node, "0.0.0")
        extended.append({"edge": f"({kh_node}, 0.0.0)", "distance": distance})

    # Step 7: Add 0.0.0 → 0.0 edge
    distance = get_fallback_distance("0.0.0", "0.0")
    extended.append({"edge": "(0.0.0, 0.0)", "distance": distance})

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

        # GR → KH
        elif src in gr_nodes and dst in kh_nodes:
            filtered.append(entry)

        # ✅ KH → GR (previously missing)
        elif src in kh_nodes and dst in gr_nodes:
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
    for edge in filtered[:min(len(filtered), 3)]:
        print(edge)

    return filtered

def annotate_component_in_time_details(time_details, gr_nodes, kh_nodes):
    enriched = []
    current_component = None

    for step in time_details:
        src = step["from"]
        dst = step["to"]
        enriched_step = step.copy()

        # GR → KH → robot places component
        if src in gr_nodes and dst in kh_nodes:
            current_component = gr_nodes[src]
            enriched_step["component_placed"] = current_component

        # 0.0 → GR → robot picks component
        elif src == "0.0" and dst in gr_nodes:
            current_component = gr_nodes[dst]
            enriched_step["component_picked"] = current_component

        # KH → GR (robot picks next component) — OPTIONAL, if needed
        elif src in kh_nodes and dst in gr_nodes:
            current_component = gr_nodes[dst]
            enriched_step["component_picked"] = current_component

        enriched.append(enriched_step)

    return enriched