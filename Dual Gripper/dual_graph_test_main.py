# ===== dual_graph_test_main.py =====
# Run: python dual_graph_test_main.py random_json_input_dual.min2.json

import json
import sys
from collections import defaultdict

# -----------------------
# your node builders (unchanged)
# -----------------------
def generate_kh_nodes(kh_sequences, kit_holder_types):
    kh_nodes = {}
    for entry in kh_sequences:
        for kh_pos, kh_id in entry.items():
            if kh_id in kit_holder_types:
                for comp in kit_holder_types[kh_id].get("contents", []):
                    if isinstance(comp, dict):
                        position = comp["position"]
                        comp_type = comp["type"]
                        kh_node = f"{kh_pos}.{position}"       # e.g., "1.1"
                        kh_nodes[kh_node] = comp_type
    return kh_nodes

def generate_gr_nodes(gr_sequence, container_types):
    gr_nodes = {}
    for entry in gr_sequence:
        for gr_pos, container_id in entry.items():        # e.g., "1.1": "Container_1"
            if container_id in container_types:
                contents = container_types[container_id].get("contents", [])
                for comp in contents:
                    if isinstance(comp, dict) and "position" in comp and "type" in comp:
                        position = comp["position"]       # "1","2","3",...
                        comp_type = comp["type"]
                        gr_node = f"{gr_pos}.{position}"   # e.g., "1.1.1"
                        gr_nodes[gr_node] = comp_type
    return gr_nodes

# -----------------------
# tiny helpers
# -----------------------
def _parse_gr(node):
    parts = node.split(".")
    if len(parts) == 3:
        return parts[0], parts[1], parts[2]   # row, col, idx
    return None, None, None

def _get_base(name):
    parts = name.split(".")
    if len(parts) == 2:              # KH like '1.1'
        return parts[0]
    if len(parts) == 3:              # GR like '1.1.1'
        return ".".join(parts[:2])   # '1.1'
    return name

def _build_lookup(min_edges):
    return {
        tuple(e["edge"].strip("()").replace("'", "").split(", ")): e["distance"]
        for e in min_edges
    }

def _get_distance(src, dst, lookup, default=10**9):
    # exact first
    if (src, dst) in lookup:
        return lookup[(src, dst)]
    bs, bd = _get_base(src), _get_base(dst)
    # base(src) + exact dst
    for (s, d), w in lookup.items():
        if _get_base(s) == bs and d == dst:
            return w
    # exact src + base(dst)
    for (s, d), w in lookup.items():
        if s == src and _get_base(d) == bd:
            return w
    # base(src) + base(dst)
    for (s, d), w in lookup.items():
        if _get_base(s) == bs and _get_base(d) == bd:
            return w
    return default

# -----------------------
# dual expansion (no self-loops; GR->GR only next index; KH->KH allowed; 0.0->*.1 only)
# -----------------------
def extend_distance_matrix_dual(gr_nodes, kh_nodes, kh_sequences_opt, min_edges, add_bias=2000):
    lookup = _build_lookup(min_edges)
    BIG = 10**8
    out = []

    gr_set = set(gr_nodes.keys())     # "r.c.i"
    kh_set = set(kh_nodes.keys())     # "c.idx" (two-part)

    # 0.0 -> GR (only *.1 like in your short list)
    for g in gr_set:
        r, c, i = _parse_gr(g)
        if i != "1":
            continue
        w = _get_distance("0.0", g, lookup)
        if w < BIG:
            out.append({"edge": f"(0.0, {g})", "distance": w + add_bias})

    # GR -> KH (type match)
    for g, t in gr_nodes.items():
        for kh, kt in kh_nodes.items():
            if t != kt:
                continue
            w = _get_distance(g, kh, lookup)
            if w < BIG:
                out.append({"edge": f"({g}, {kh})", "distance": w + add_bias})

    # KH -> GR (all)
    for kh in kh_set:
        for g in gr_set:
            w = _get_distance(kh, g, lookup)
            if w < BIG:
                out.append({"edge": f"({kh}, {g})", "distance": w + add_bias})

    # KH -> 0.0.0
    for kh in kh_set:
        w = _get_distance(kh, "0.0.0", lookup)
        if w < BIG:
            out.append({"edge": f"({kh}, 0.0.0)", "distance": w + add_bias})

    # 0.0.0 -> 0.0
    w = _get_distance("0.0.0", "0.0", lookup)
    if w < BIG:
        out.append({"edge": "(0.0.0, 0.0)", "distance": w})

    # KH -> KH (no self)
    kh_faces = list(kh_set)
    for u in kh_faces:
        for v in kh_faces:
            if u == v:
                continue
            w = _get_distance(u, v, lookup)
            if w < BIG:
                out.append({"edge": f"({u}, {v})", "distance": w})

    # GR -> GR (same base, next index only, no self)
    by_base = defaultdict(set)
    for g in gr_set:
        r, c, i = _parse_gr(g)
        if r is None:
            continue
        by_base[f"{r}.{c}"].add(int(i))

    for base, idxs in by_base.items():
        for k in sorted(idxs):
            nxt = k + 1
            if nxt in idxs:
                u = f"{base}.{k}"
                v = f"{base}.{nxt}"
                w = _get_distance(u, v, lookup)
                if w < BIG:
                    out.append({"edge": f"({u}, {v})", "distance": w})

    # remove any accidental self loops
    cleaned = []
    for e in out:
        s, d = e["edge"].strip("()").split(", ")
        if s != d:
            cleaned.append(e)
    return cleaned

# -----------------------
# build edges from your specific input shape
# -----------------------
def build_edges_from_input(data):
    templates = data.get("templates", {})
    containers = templates.get("containers_opt", data.get("containers_opt", {}))
    kit_holders = templates.get("kit_holders_opt", data.get("kit_holders_opt", {}))
    kh_sequences_opt = templates.get("kh_sequences_opt", data.get("kh_sequences_opt", []))
    min_edges = data.get("distance_matrix_min", templates.get("distance_matrix_min", []))

    gr_nodes = generate_gr_nodes(data["gr_sequence"], containers)
    kh_nodes = generate_kh_nodes(kh_sequences_opt, kit_holders)

    edges = extend_distance_matrix_dual(
        gr_nodes=gr_nodes,
        kh_nodes=kh_nodes,
        kh_sequences_opt=kh_sequences_opt,
        min_edges=min_edges,
        add_bias=2000,
    )
    return edges, gr_nodes, kh_nodes

# -----------------------
# RULE CHECKS / PRINTS
# -----------------------
def check_rules(edges, gr_nodes, kh_nodes):
    gr_set = set(gr_nodes.keys())
    kh_set = set(kh_nodes.keys())
    lookup_type_gr = gr_nodes
    lookup_type_kh = kh_nodes

    violations = []

    # helper parsers
    def parse_edge(e):
        s, d = e["edge"].strip("()").split(", ")
        return s.strip(), d.strip()

    # 1) no self loops
    for e in edges:
        s, d = parse_edge(e)
        if s == d:
            violations.append(f"SELF-LOOP: {s} -> {d}")

    # 2) 0.0 -> GR only when index == 1
    for e in edges:
        s, d = parse_edge(e)
        if s == "0.0" and d in gr_set:
            _, _, i = _parse_gr(d)
            if i != "1":
                violations.append(f"0.0→GR not .1 index: {e}")

    # 3) GR -> KH type match
    for e in edges:
        s, d = parse_edge(e)
        if s in gr_set and d in kh_set:
            if lookup_type_gr[s] != lookup_type_kh[d]:
                violations.append(f"GR→KH type mismatch: {s}({lookup_type_gr[s]}) -> {d}({lookup_type_kh[d]})")

    # 4) GR -> GR only same base and next index
    for e in edges:
        s, d = parse_edge(e)
        if s in gr_set and d in gr_set:
            rb, cb, i1 = _parse_gr(s)
            ra, ca, i2 = _parse_gr(d)
            if (rb, cb) != (ra, ca) or int(i2) != int(i1) + 1:
                violations.append(f"GR→GR wrong step: {s} -> {d}")

    # 5) KH -> KH allowed (already), just ensure no self (covered in 1)
    #    Optionally ensure both are KH
    for e in edges:
        s, d = parse_edge(e)
        if s in kh_set and d in kh_set and s == d:
            violations.append(f"KH→KH self? {s} -> {d}")

    # 6) require (0.0.0 -> 0.0) exists
    if not any(e["edge"] == "(0.0.0, 0.0)" for e in edges):
        violations.append("Missing required edge: (0.0.0, 0.0)")

    return violations

# -----------------------
# MAIN
# -----------------------
def main():
    # allow running with no CLI args by falling back to a default file
    default_json = "random_json_input_dual.min2.json"  # <- set your default here

    if len(sys.argv) < 2:
        json_path = default_json
        print(f"(no arg given) → using default JSON: {json_path}")
    else:
        json_path = sys.argv[1]

    with open(json_path) as f:
        msg = json.load(f)

    data = msg.get("data", msg)  # allow either top-level or wrapped under "data"

    edges, gr_nodes, kh_nodes = build_edges_from_input(data)

    print(f"✅ Built nodes: GR={len(gr_nodes)}, KH={len(kh_nodes)}")
    print(f"✅ Total candidate edges: {len(edges)}")
    print("— sample edges —")
    for e in edges[:min(10, len(edges))]:
        print("  ", e)

    violations = check_rules(edges, gr_nodes, kh_nodes)
    if violations:
        print("\n❌ RULE CHECKS FAILED:")
        for v in violations[:50]:
            print("  -", v)
        if len(violations) > 50:
            print(f"  ... and {len(violations)-50} more")
    else:
        print("\n✅ All rule checks passed.")

    try:
        from parse_json_dual import create_distance_matrices
        from GraphCreation_dual import create_directed_bipartite_graph

        a_to_b_matrix = create_distance_matrices({"data": {"distance_matrix": edges}})
        # Use the real KH slot nodes that exist in the matrix (e.g. '1.1','1.2',...,'4.5')
        kit_holders_tpl = data.get("templates", {}).get("kit_holders_opt", data.get("kit_holders_opt", {}))
        kh_seq = data.get("templates", {}).get("kh_sequences_opt", data.get("kh_sequences_opt", []))

        # Build KH nodes exactly like you do earlier
        kh_nodes = generate_kh_nodes(kh_seq, kit_holders_tpl)  # dict like {'1.1': 'Component_5', ...}
        active_kh_nodes = sorted(kh_nodes.keys())

        # Optional safety check
        missing = [n for n in active_kh_nodes if n not in a_to_b_matrix.index or n not in a_to_b_matrix.columns]
        assert not missing, f"KH nodes not in matrix: {missing}"

        B, set_1, set_2 = create_directed_bipartite_graph(a_to_b_matrix, active_kh_nodes)

        print(f"\n📈 Graph built: |V|={len(B.nodes)}, |E|={len(B.edges)}")
        print(f"Set 1 size: {len(set_1)} | Set 2 size: {len(set_2)}")

    except ImportError:
        print("\n(ℹ️ Skipped graph build — imports not available in this test context.)")

if __name__ == "__main__":
    main()
