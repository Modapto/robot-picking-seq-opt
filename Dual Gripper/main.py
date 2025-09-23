import json
import sys
from collections import defaultdict, Counter
from parse_json_dual import create_distance_matrices
from GraphCreation_dual import create_directed_bipartite_graph
from dual_gripper_heuristic import nearest_tsp_dual, total_cost


# ----------------- helpers you already had -----------------

def parse_gr_node(n: str):
    # '2.5.16' -> base='2.5', pos=16 (int)
    a, b, c = n.split(".")
    return f"{a}.{b}", int(c)

def prune_gr_nodes_to_demand(gr_nodes: dict, kh_nodes: dict) -> dict:
    """
    Keep only the first-needed GR pockets by type to exactly cover KH demand.
    Prefers earliest pockets (smallest position) and earlier lanes.
    """
    demand = Counter(kh_nodes.values())  # type -> count needed

    # (type, base, pos, node) sorted by type, lane, pocket index
    rows = []
    for node, comp_type in gr_nodes.items():
        base, pos = parse_gr_node(node)
        rows.append((comp_type, base, pos, node))
    rows.sort(key=lambda x: (x[0], x[1], x[2]))

    keep = set()
    taken = Counter()
    for t, base, pos, node in rows:
        need = demand.get(t, 0)
        if need <= 0:
            continue
        if taken[t] < need:
            keep.add(node)
            taken[t] += 1

    # Return only kept nodes
    return {n: gr_nodes[n] for n in keep}


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

def _parse_gr(node):
    parts = node.split(".")
    if len(parts) == 3:
        return parts[0], parts[1], parts[2]
    return None, None, None

def _get_base(name):
    parts = name.split(".")
    if len(parts) == 2:
        return parts[0]
    if len(parts) == 3:
        return ".".join(parts[:2])
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

# dual expansion (no self-loops; GR->GR only next index; KH->KH allowed; 0.0->*.1 only)
def extend_distance_matrix_dual(gr_nodes, kh_nodes, kh_sequences_opt, min_edges, add_bias=2000):
    lookup = _build_lookup(min_edges)
    BIG = 10**8
    out = []

    gr_set = set(gr_nodes.keys())
    kh_set = set(kh_nodes.keys())

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

    cleaned = []
    for e in out:
        s, d = e["edge"].strip("()").split(", ")
        if s != d:
            cleaned.append(e)
    return cleaned


def build_edges_from_input(data, use_prune=True):
    templates = data.get("templates", {})
    containers = templates.get("containers_opt", data.get("containers_opt", {}))
    kit_holders = templates.get("kit_holders_opt", data.get("kit_holders_opt", {}))
    kh_sequences_opt = templates.get("kh_sequences_opt", data.get("kh_sequences_opt", []))
    min_edges = data.get("distance_matrix_min", templates.get("distance_matrix_min", []))

    # Build KH/GR maps
    gr_nodes_full = generate_gr_nodes(data["gr_sequence"], containers)
    kh_nodes = generate_kh_nodes(kh_sequences_opt, kit_holders)

    # NEW: prune GR pockets to exactly KH demand (so we won't pick deep pockets)
    gr_nodes = prune_gr_nodes_to_demand(gr_nodes_full, kh_nodes) if use_prune else gr_nodes_full
    if use_prune:
        print(f"🔧 GR pruning: kept {len(gr_nodes)} of {len(gr_nodes_full)} pockets to match KH demand")

    # Build edges on the (possibly) pruned GR set
    edges = extend_distance_matrix_dual(
        gr_nodes=gr_nodes,
        kh_nodes=kh_nodes,
        kh_sequences_opt=kh_sequences_opt,
        min_edges=min_edges,
        add_bias=2000,
    )
    return edges, gr_nodes, kh_nodes


def check_rules(edges, gr_nodes, kh_nodes):
    gr_set = set(gr_nodes.keys())
    kh_set = set(kh_nodes.keys())
    lookup_type_gr = gr_nodes
    lookup_type_kh = kh_nodes

    violations = []

    def parse_edge(e):
        s, d = e["edge"].strip("()").split(", ")
        return s.strip(), d.strip()

    # no self loops
    for e in edges:
        s, d = parse_edge(e)
        if s == d:
            violations.append(f"SELF-LOOP: {s} -> {d}")

    # 0.0 -> GR only when index == 1
    for e in edges:
        s, d = parse_edge(e)
        if s == "0.0" and d in gr_set:
            _, _, i = _parse_gr(d)
            if i != "1":
                violations.append(f"0.0→GR not .1 index: {e}")

    # GR -> KH type match
    for e in edges:
        s, d = parse_edge(e)
        if s in gr_set and d in kh_set:
            if lookup_type_gr[s] != lookup_type_kh[d]:
                violations.append(f"GR→KH type mismatch: {s}({lookup_type_gr[s]}) -> {d}({lookup_type_kh[d]})")

    # GR -> GR only same base and next index
    for e in edges:
        s, d = parse_edge(e)
        if s in gr_set and d in gr_set:
            rb, cb, i1 = _parse_gr(s)
            ra, ca, i2 = _parse_gr(d)
            if (rb, cb) != (ra, ca) or int(i2) != int(i1) + 1:
                violations.append(f"GR→GR wrong step: {s} -> {d}")

    # require 0.0.0 -> 0.0 exists
    if not any(e["edge"] == "(0.0.0, 0.0)" for e in edges):
        violations.append("Missing required edge: (0.0.0, 0.0)")

    return violations


def main():
    default_json = "random_json_input_dual.min2.json"  # <- set your default here

    if len(sys.argv) < 2:
        json_path = default_json
        print(f"(no arg given) → using default JSON: {json_path}")
    else:
        json_path = sys.argv[1]

    with open(json_path) as f:
        msg = json.load(f)

    data = msg.get("data", msg)

    edges, gr_nodes, kh_nodes = build_edges_from_input(data, use_prune=True)

    print(f"Built nodes: GR={len(gr_nodes)}, KH={len(kh_nodes)}")
    print(f"Total candidate edges: {len(edges)}")
    print("— sample edges —")
    for e in edges[:min(855, len(edges))]:
        print("  ", e)

    violations = check_rules(edges, gr_nodes, kh_nodes)
    if violations:
        print("RULE CHECKS FAILED:")
        for v in violations[:50]:
            print("  -", v)
        if len(violations) > 50:
            print(f"  ... and {len(violations)-50} more")
    else:
        print("All rule checks passed.")

    # ---- optional: build graph + run your NN heuristic ----
    try:

        a_to_b_matrix = create_distance_matrices({"data": {"distance_matrix": edges}})

        # KH nodes (slot ids) to pass to your graph builder
        kit_holders_tpl = data.get("templates", {}).get("kit_holders_opt", data.get("kit_holders_opt", {}))
        kh_seq = data.get("templates", {}).get("kh_sequences_opt", data.get("kh_sequences_opt", []))
        kh_nodes_again = generate_kh_nodes(kh_seq, kit_holders_tpl)
        active_kh_nodes = sorted(kh_nodes_again.keys())

        # sanity: these KH slots should exist in matrix axes
        missing = [n for n in active_kh_nodes if n not in a_to_b_matrix.index or n not in a_to_b_matrix.columns]
        assert not missing, f"KH nodes not in matrix: {missing}"

        B, set_1, set_2 = create_directed_bipartite_graph(a_to_b_matrix, active_kh_nodes)

        print(f"Graph built: |V|={len(B.nodes)}, |E|={len(B.edges)}")
        print(f"Set 1 size: {len(set_1)} | Set 2 size: {len(set_2)}")

        tour = nearest_tsp_dual(
            G=B,
            start="0.0",
            end="0.0.0",
            set_kh=set_1,          # KH from graph creation
            set_gr=set_2,          # GR from graph creation (already pruned)
            gr_types=gr_nodes,     # pruned GR type map
            kh_types=kh_nodes,     # KH type map
            max_load=2,
            verbose=True
        )
        cost, details = total_cost(B, tour)
        print("tour:", tour)
        print("cost:", cost)

    except ImportError:
        print("Skipped graph build — imports not available in this test context.)")


if __name__ == "__main__":
    main()
