import json
import sys
from collections import defaultdict, Counter
from parse_json_dual import create_distance_matrices
from GraphCreation_dual import create_directed_bipartite_graph
from dual_gripper_heuristic import nearest_tsp_dual, total_cost


# ====== CONFIG ======
DEFAULT_JSON = "input_dual_gripper.json"
ADD_EDGE_BIAS = 2000
ALLOW_CROSS_RACK_GR_PICK2 = True     # allow GR→GR across different bases (pick→pick)
CROSS_GR_EXTRA_BIAS = 0              # optional penalty for GR→GR hops across racks
USE_PRUNE = True                     # prune GR pockets to exactly KH demand
OUTPUT_PATH = "output_dual.json"

# ====================


# ---------- helpers ----------
def parse_gr_node(n: str):
    # '2.5.16' -> base='2.5', pos=16 (int)
    a, b, c = n.split(".")
    return f"{a}.{b}", int(c)

def prune_gr_nodes_to_demand(gr_nodes: dict, kh_nodes: dict) -> dict:
    """Keep only the first-needed GR pockets by type to exactly cover KH demand."""
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
                        kh_nodes[f"{kh_pos}.{position}"] = comp_type
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
                        gr_nodes[f"{gr_pos}.{position}"] = comp_type
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

def extend_distance_matrix_dual(
    gr_nodes,
    kh_nodes,
    kh_sequences_opt,
    min_edges,
    add_bias=ADD_EDGE_BIAS,
    allow_cross_rack_gr_pick2=ALLOW_CROSS_RACK_GR_PICK2,
    cross_gr_extra_bias=CROSS_GR_EXTRA_BIAS
):
    lookup = _build_lookup(min_edges)
    BIG = 10**8
    out = []

    gr_set = set(gr_nodes.keys())
    kh_set = set(kh_nodes.keys())

    # 0.0 -> GR (only *.1)
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

    # GR -> GR
    # (a) same-base next-index hops only
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

    # (b) cross-rack GR→GR (never within the same base)
    if allow_cross_rack_gr_pick2:
        gr_list = list(gr_set)
        for u in gr_list:
            ru, cu, iu = _parse_gr(u)
            if ru is None:
                continue
            for v in gr_list:
                if u == v:
                    continue
                rv, cv, iv = _parse_gr(v)
                if rv is None:
                    continue
                if (ru, cu) == (rv, cv):
                    continue  # within-base handled in (a); everything else forbidden
                w = _get_distance(u, v, lookup)
                if w < BIG:
                    out.append({"edge": f"({u}, {v})", "distance": w + cross_gr_extra_bias})

    # remove self loops
    cleaned = []
    for e in out:
        s, d = e["edge"].strip("()").split(", ")
        if s != d:
            cleaned.append(e)
    return cleaned

def build_edges_from_input(data, use_prune=USE_PRUNE):
    templates = data.get("templates", {})
    containers = templates.get("containers_opt", data.get("containers_opt", {}))
    kit_holders = templates.get("kit_holders_opt", data.get("kit_holders_opt", {}))
    kh_sequences_opt = templates.get("kh_sequences_opt", data.get("kh_sequences_opt", []))
    min_edges = data.get("distance_matrix_min", templates.get("distance_matrix_min", []))

    # Build KH/GR maps
    gr_nodes_full = generate_gr_nodes(data["gr_sequence"], containers)
    kh_nodes = generate_kh_nodes(kh_sequences_opt, kit_holders)

    # Prune GR to demand
    gr_nodes = prune_gr_nodes_to_demand(gr_nodes_full, kh_nodes) if use_prune else gr_nodes_full
    if use_prune:
        print(f"🔧 GR pruning: kept {len(gr_nodes)} of {len(gr_nodes_full)} pockets to match KH demand")

    # Build edges on the chosen GR set
    edges = extend_distance_matrix_dual(
        gr_nodes=gr_nodes,
        kh_nodes=kh_nodes,
        kh_sequences_opt=kh_sequences_opt,
        min_edges=min_edges,
        add_bias=ADD_EDGE_BIAS,
        allow_cross_rack_gr_pick2=ALLOW_CROSS_RACK_GR_PICK2,
        cross_gr_extra_bias=CROSS_GR_EXTRA_BIAS
    )
    return edges, gr_nodes, kh_nodes

def check_rules(edges, gr_nodes, kh_nodes, allow_cross_rack_gr_pick2=ALLOW_CROSS_RACK_GR_PICK2):
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

    # GR -> GR rule
    for e in edges:
        s, d = parse_edge(e)
        if s in gr_set and d in gr_set:
            rb, cb, i1 = _parse_gr(s)
            ra, ca, i2 = _parse_gr(d)
            if allow_cross_rack_gr_pick2:
                # Only forbid within-same-base if it is not next index
                if (rb, cb) == (ra, ca) and int(i2) != int(i1) + 1:
                    violations.append(f"GR→GR wrong step (same-base must be +1): {s} -> {d}")
            else:
                # Strict: must be same base AND next index
                if (rb, cb) != (ra, ca) or int(i2) != int(i1) + 1:
                    violations.append(f"GR→GR wrong step: {s} -> {d}")

    # require 0.0.0 -> 0.0
    if not any(e["edge"] == "(0.0.0, 0.0)" for e in edges):
        violations.append("Missing required edge: (0.0.0, 0.0)")

    return violations

# def main():
#     if len(sys.argv) < 2:
#         json_path = DEFAULT_JSON
#         print(f"(no arg given) → using default JSON: {json_path}")
#     else:
#         json_path = sys.argv[1]
#
#     with open(json_path) as f:
#         msg = json.load(f)
#
#     data = msg.get("data", msg)
#
#     edges, gr_nodes, kh_nodes = build_edges_from_input(data, use_prune=USE_PRUNE)
#
#     print(f"Built nodes: GR={len(gr_nodes)}, KH={len(kh_nodes)}")
#     print(f"Total candidate edges: {len(edges)}")
#     print("— sample edges —")
#     for e in edges[:min(5, len(edges))]:
#         print("  ", e)
#
#     violations = check_rules(edges, gr_nodes, kh_nodes, allow_cross_rack_gr_pick2=ALLOW_CROSS_RACK_GR_PICK2)
#     if violations:
#         hdr = "RULE CHECKS FAILED (cross-rack GR→GR allowed):" if ALLOW_CROSS_RACK_GR_PICK2 else "RULE CHECKS FAILED:"
#         print(hdr)
#         for v in violations[:50]:
#             print("  -", v)
#         if len(violations) > 50:
#             print(f"  ... and {len(violations)-50} more")
#     else:
#         print("All rule checks passed.")
#
#     # ---- build graph + run NN heuristic ----
#     a_to_b_matrix = create_distance_matrices({"data": {"distance_matrix": edges}})
#
#     # KH nodes (slot ids) to pass to your graph builder
#     kit_holders_tpl = data.get("templates", {}).get("kit_holders_opt", data.get("kit_holders_opt", {}))
#     kh_seq = data.get("templates", {}).get("kh_sequences_opt", data.get("kh_sequences_opt", []))
#     kh_nodes_again = generate_kh_nodes(kh_seq, kit_holders_tpl)
#     active_kh_nodes = sorted(kh_nodes_again.keys())
#
#     # sanity: these KH slots should exist in matrix axes
#     missing = [n for n in active_kh_nodes if n not in a_to_b_matrix.index or n not in a_to_b_matrix.columns]
#     assert not missing, f"KH nodes not in matrix: {missing}"
#
#     B, set_1, set_2 = create_directed_bipartite_graph(a_to_b_matrix, active_kh_nodes)
#
#     print(f"Graph built: |V|={len(B.nodes)}, |E|={len(B.edges)}")
#     print(f"Set 1 size: {len(set_1)} | Set 2 size: {len(set_2)}")
#
#     tour = nearest_tsp_dual(
#         G=B,
#         start="0.0",
#         end="0.0.0",
#         set_kh=set_1,          # KH from graph creation
#         set_gr=set_2,          # GR from graph creation (already pruned)
#         gr_types=gr_nodes,     # pruned GR type map
#         kh_types=kh_nodes,     # KH type map
#         max_load=2,
#         verbose=True
#     )
#     cost, details = total_cost(B, tour)
#     print("tour:", tour)
#     print("cost:", cost)
#
#
# if __name__ == "__main__":
#     main()

# ---------- time-details + output helpers ----------
def node_kind(node, gr_types, kh_types):
    if node in gr_types:
        return "GR"
    if node in kh_types:
        return "KH"
    if node in ("0.0", "0.0.0"):
        return "HOME"
    return "OTHER"

def edge_weight(G, u, v):
    return int(G[u][v]["weight"])

def build_time_details_from_tour(G, tour, gr_types, kh_types):
    """
    Emit rows like the single-gripper pilot output:
      - ARRIVE at a GR node -> component_picked
      - ARRIVE at a KH node -> component_placed
      - Moves to HOME nodes only carry distance
    """
    rows = []
    for i in range(len(tour) - 1):
        u, v = tour[i], tour[i + 1]
        dist = edge_weight(G, u, v)
        kind = node_kind(v, gr_types, kh_types)
        row = {"from": u, "to": v, "distance": dist}
        if kind == "GR":
            row["component_picked"] = gr_types[v]
        elif kind == "KH":
            row["component_placed"] = kh_types[v]
        rows.append(row)
    return rows


def main():
    if len(sys.argv) < 2:
        json_path = DEFAULT_JSON
        print(f"(no arg given) → using default JSON: {json_path}")
    else:
        json_path = sys.argv[1]

    with open(json_path) as f:
        msg = json.load(f)

    data = msg.get("data", msg)

    edges, gr_nodes, kh_nodes = build_edges_from_input(data, use_prune=USE_PRUNE)

    print(f"Built nodes: GR={len(gr_nodes)}, KH={len(kh_nodes)}")
    print(f"Total candidate edges: {len(edges)}")
    print("— sample edges —")
    for e in edges[:min(5, len(edges))]:
        print("  ", e)

    violations = check_rules(edges, gr_nodes, kh_nodes, allow_cross_rack_gr_pick2=ALLOW_CROSS_RACK_GR_PICK2)
    if violations:
        hdr = "RULE CHECKS FAILED (cross-rack GR→GR allowed):" if ALLOW_CROSS_RACK_GR_PICK2 else "RULE CHECKS FAILED:"
        print(hdr)
        for v in violations[:50]:
            print("  -", v)
        if len(violations) > 50:
            print(f"  ... and {len(violations)-50} more")
    else:
        print("All rule checks passed.")

    # ---- build graph + run NN heuristic ----
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
    print("cost:", int(cost))

    # ---- build pilot-like JSON output (time_details only addition) ----
    time_details = build_time_details_from_tour(B, tour, gr_nodes, kh_nodes)

    output = {
        "optimization_run": True,
        "message": "Valid KH sequence optimization (dual-gripper) starts...",
        "solutionTime": int(cost),   # replace with real timing if available
        "totalTime": int(cost),      # replace with real timing if available
        "optimization_results": {
            "exact": {
                "cost": int(cost),
                "time_details": time_details
            },
            "improvement_percentage": 0.0
        }
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=4)
    print(f"\n✅ Wrote dual-gripper output to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()