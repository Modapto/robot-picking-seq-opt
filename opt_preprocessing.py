# REPOSITORY NAME (c) by the University of Piraues, Greece.
#
# REPOSITORY NAME is licensed under a
# Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <http://creativecommons.org/licenses/by-nc-nd/3.0/>.

# Generate KH node IDs and their component types.
#
# For each KH position in `kh_sequences`, this function:
#   - Looks up the corresponding KH template in `kit_holder_types`,
#   - Reads its `contents` list,
#   - Builds node names of the form "<kh_pos>.<position>" (e.g. "1.3"),
#   - Maps each node name to its component type.
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
    """
    Generate GR node IDs and their component types.

    For each GR position in `gr_sequence`, this function:
      - Finds the corresponding container in `container_types`,
      - Reads its `contents`,
      - Builds node names of the form "<gr_pos>.<position>" (e.g. "2.7.3"),
      - Maps each node name to its component type.
    """
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
    """
     Extend a base distance matrix with GR/KH-specific edges.

     The function:
       - Builds a lookup from the original matrix of edges "(src, dst)" → distance.
       - Defines a smart fallback rule to infer distances when an exact edge is missing,
         using base coordinates (e.g. "1.1.2" → "1.1").
       - Adds:
           * 0.0 → GR edges,
           * GR → KH edges (for matching component types),
           * KH → GR edges (all combinations),
           * KH → 0.0.0 edges,
           * 0.0.0 → 0.0 edge.

     All newly added edges are stored as dicts with "edge" and "distance" keys.
     """
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
        extended.append({"edge": f"(0.0, {gr_node})", "distance": distance + 2000})

    # Step 4: Add GR → KH edges (if types match)
    for gr_node, gr_type in gr_nodes.items():
        for kh_node, kh_type in kh_nodes.items():
            if gr_type == kh_type:
                distance = get_fallback_distance(gr_node, kh_node)
                extended.append({"edge": f"({gr_node}, {kh_node})", "distance": distance + 2000})

    # Step 5: Add KH → GR edges (ALL combinations, regardless of type)
    for kh_node in kh_nodes:
        for gr_node in gr_nodes:
            distance = get_fallback_distance(kh_node, gr_node)
            extended.append({"edge": f"({kh_node}, {gr_node})", "distance": distance + 2000})

    # Step 6: Add KH → 0.0.0 edges
    for kh_node in kh_nodes:
        distance = get_fallback_distance(kh_node, "0.0.0")
        extended.append({"edge": f"({kh_node}, 0.0.0)", "distance": distance + 2000})

    # Step 7: Add 0.0.0 → 0.0 edge
    distance = get_fallback_distance("0.0.0", "0.0")
    extended.append({"edge": "(0.0.0, 0.0)", "distance": distance})

    return extended

def generate_filtered_distance_matrix(extended_matrix, gr_nodes, kh_nodes):
    """
    Filter an extended distance matrix to keep only valid BTSP edges.

    Rules kept:
      - 0.0 → GR
      - GR → KH
      - KH → GR
      - KH → 0.0.0
      - 0.0.0 → 0.0
    """
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

        # KH → GR (previously missing)
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
    """
    Add component pick/place information to time detail steps.

    For each movement step:
      - GR → KH: marks "component_placed" with the GR component type.
      - 0.0 → GR: marks "component_picked" with the GR component type.
      - KH → GR: marks "component_picked" with the GR component type (next pick).
    """
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


def validate_component_availability(kh_sequences, kit_holder_types, container_types):
    """
    Validate that the requested KH sequences can be fulfilled by available containers.

    The function:
      - Counts how many components of each type are required by all KHs in
        `kh_sequences` (based on `kit_holder_types`),
      - Counts how many components of each type are available in `container_types`,
      - Detects over-requested component types (required > available).
    """
    from collections import Counter

    if kh_sequences and isinstance(kh_sequences[0], list):
        flat_sequences = [item for phase in kh_sequences for item in phase]
    else:
        flat_sequences = kh_sequences

    required = Counter()
    for entry in flat_sequences:
        for _, kh_id in entry.items():
            if kh_id in kit_holder_types:
                for item in kit_holder_types[kh_id].get("contents", []):
                    if isinstance(item, dict):
                        required[item["type"]] += 1

    available = Counter()
    for container in container_types.values():
        for item in container.get("contents", []):
            if isinstance(item, dict):
                available[item["type"]] += 1

    over_requested = {}
    for comp, req_qty in required.items():
        if req_qty > available.get(comp, 0):
            over_requested[comp] = (req_qty, available.get(comp, 0))

    if over_requested:
        message_lines = ["This KH sequence is unavailable to run due to over-requested components:"]
        for comp, (req, avail) in over_requested.items():
            message_lines.append(f"  - {comp}: requested {req}, available {avail}")
        message = "".join(message_lines)
        print("Message: ", message)
        return False, message

    return True, ""
