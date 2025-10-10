import json, sys, random
from collections import defaultdict, Counter
from time import time

from parse_json_dual import create_distance_matrices
from GraphCreation_dual import create_directed_bipartite_graph
from dual_gripper_heuristic import nearest_tsp_dual
from linear_dual import linear_picking_dual

# ====== CONFIG ======
INPUT_PATH = "input_dual.json"
OUTPUT_PATH = "dual_optimization_output.json"

ADD_EDGE_BIAS = 2000                 # small constant to avoid zero-weights in composed edges
ALLOW_CROSS_RACK_GR_PICK2 = True     # allow GR→GR across different bases (pick→pick)
CROSS_GR_EXTRA_BIAS = 0              # optional penalty for GR→GR hops across racks
USE_PRUNE = True                     # prune GR pockets to exactly KH demand
# ====================


# ---------- helpers ----------
def parse_gr_node(n: str):
    # '2.5.16' -> base='2.5', pos=16 (int)
    a, b, c = n.split(".")
    return f"{a}.{b}", int(c)

def prune_gr_nodes_to_demand(gr_nodes: dict, kh_nodes: dict) -> dict:
    """Keep only the first-needed GR pockets by type to exactly cover KH demand."""
    demand = Counter(kh_nodes.values())  # type -> count needed
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
    cross_gr_extra_bias=CROSS_GR_EXTRA_BIAS,
    require_type_match_gr_kh=False   # RELAXED for both methods
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

    # GR -> KH (RELAXED: allow all edges, or restrict to type matches if required)
    for g, t in gr_nodes.items():
        for kh, kt in kh_nodes.items():
            if require_type_match_gr_kh and (t != kt):
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
                    continue
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

def build_edges_from_input(data, use_prune=USE_PRUNE, require_type_match_gr_kh=False):
    templates = data.get("templates", {})
    containers = templates.get("containers_opt", data.get("containers_opt", {}))
    kit_holders = templates.get("kit_holders_opt", data.get("kit_holders_opt", {}))
    kh_sequences_opt = templates.get("kh_sequences_opt", data.get("kh_sequences_opt", []))
    min_edges = data.get("distance_matrix_min", templates.get("distance_matrix_min", []))

    gr_nodes_full = generate_gr_nodes(data["gr_sequence"], containers)
    kh_nodes = generate_kh_nodes(kh_sequences_opt, kit_holders)

    gr_nodes = prune_gr_nodes_to_demand(gr_nodes_full, kh_nodes) if use_prune else gr_nodes_full
    print(f"🔧 GR pruning: kept {len(gr_nodes)} of {len(gr_nodes_full)} pockets to match KH demand")

    edges = extend_distance_matrix_dual(
        gr_nodes=gr_nodes,
        kh_nodes=kh_nodes,
        kh_sequences_opt=kh_sequences_opt,
        min_edges=min_edges,
        add_bias=ADD_EDGE_BIAS,
        allow_cross_rack_gr_pick2=ALLOW_CROSS_RACK_GR_PICK2,
        cross_gr_extra_bias=CROSS_GR_EXTRA_BIAS,
        require_type_match_gr_kh=require_type_match_gr_kh,
    )
    return edges, gr_nodes, kh_nodes

def build_time_details_from_tour(G, tour, gr_types, kh_types):
    rows = []
    for i in range(len(tour) - 1):
        u, v = tour[i], tour[i + 1]
        w = int(G[u][v]["weight"]) if (u in G and v in G[u]) else 10**9
        row = {"from": u, "to": v, "distance": w}
        if v in gr_types:
            row["component_picked"] = gr_types[v]
        elif v in kh_types:
            row["component_placed"] = kh_types[v]
        rows.append(row)
    return rows

def compute_path_cost(G, tour):
    cost = 0
    for i in range(len(tour) - 1):
        u, v = tour[i], tour[i + 1]
        cost += int(G[u][v]["weight"])
    return cost


def main():
    # load input
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = INPUT_PATH

    with open(path) as f:
        msg = json.load(f)
    data = msg.get("data", msg)

    method = data.get("method", "heuristic")
    if method not in ("heuristic", "linear", "heuristic-linear"):
        raise ValueError("method must be one of: 'heuristic', 'linear', 'heuristic-linear'")

    # build edges & graph
    edges, gr_types, kh_types = build_edges_from_input(
        data, use_prune=USE_PRUNE, require_type_match_gr_kh=False
    )

    a_to_b_matrix = create_distance_matrices({"data": {"distance_matrix": edges}})

    templates = data.get("templates", {})
    kit_holders_tpl = templates.get("kit_holders_opt", data.get("kit_holders_opt", {}))
    kh_seq = templates.get("kh_sequences_opt", data.get("kh_sequences_opt", []))
    kh_nodes_again = generate_kh_nodes(kh_seq, kit_holders_tpl)
    active_kh_nodes = sorted(kh_nodes_again.keys())

    missing = [n for n in active_kh_nodes if n not in a_to_b_matrix.index or n not in a_to_b_matrix.columns]
    if missing:
        raise ValueError(f"KH nodes not in matrix: {missing}")

    B, set_1, set_2 = create_directed_bipartite_graph(a_to_b_matrix, active_kh_nodes)

    start_node = "0.0"
    end_node = "0.0.0"

    results = {}
    t0 = int(time() * 1000)

    # heuristic
    if method in ("heuristic", "heuristic-linear"):
        tour_h = nearest_tsp_dual(
            G=B,
            start=start_node,
            end=end_node,
            set_kh=set_1,
            set_gr=set_2,
            gr_types=gr_types,
            kh_types=kh_types,
            max_load=2,
            verbose=False
        )
        cost_h = compute_path_cost(B, tour_h)
        time_details_h = build_time_details_from_tour(B, tour_h, gr_types, kh_types)
        results["heuristic"] = {"cost": cost_h, "tour": tour_h, "time_details": time_details_h}

    # linear
    if method in ("linear", "heuristic-linear"):
        lin = linear_picking_dual(
            B=B,
            start_node=start_node,
            end_node=end_node,
            set_kh=set_1,
            set_gr=set_2,
            gr_types=gr_types,
            kh_types=kh_types,
            filtered_matrix=edges
        )
        tour_l = lin["tour"]
        cost_l = lin.get("total_cost", compute_path_cost(B, tour_l))
        time_details_l = build_time_details_from_tour(B, tour_l, gr_types, kh_types)
        results["linear"] = {"cost": cost_l, "tour": tour_l, "time_details": time_details_l}

    # if compare, keep winner + improvement
    if method == "heuristic-linear" and ("heuristic" in results) and ("linear" in results):
        c_h = results["heuristic"]["cost"]
        c_l = results["linear"]["cost"]
        improvement = round(((c_l - c_h) / c_l) * 100, 4) if c_l else 0.0
        if improvement > 0:
            results = {"heuristic": results["heuristic"], "improvement_percentage": improvement}
        else:
            results = {"linear": results["linear"], "improvement_percentage": improvement}

    out = {
        "optimization_run": True,
        "message": f"Ran method '{method}' successfully.",
        "solutionTime": (int(time() * 1000) - t0),
        "totalTime": (int(time() * 1000) - t0),
        "optimization_results": results
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(out, f, indent=2)
    print(f"Wrote {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
