import json, sys, random
from time import time
from copy import deepcopy
from collections import defaultdict, Counter

from parse_json_dual import create_distance_matrices
from GraphCreation_dual import create_directed_bipartite_graph
from dual_gripper_heuristic import nearest_tsp_dual
from linear_dual import linear_picking_dual

# ====== CONFIG ======
INPUT_PATH = "input_dual_gripper.json"
OUTPUT_PATH = "dual_simulation_output.json"

ADD_EDGE_BIAS = 2000
ALLOW_CROSS_RACK_GR_PICK2 = True
CROSS_GR_EXTRA_BIAS = 0
USE_PRUNE = True

N_PHASES = 20         # how many randomized GR layouts to test
SEED = 12345
# ====================


# ---- helpers (same as in optimization main; trimmed for brevity) ----
def parse_gr_node(n: str):
    a, b, c = n.split(".")
    return f"{a}.{b}", int(c)

def prune_gr_nodes_to_demand(gr_nodes: dict, kh_nodes: dict) -> dict:
    demand = Counter(kh_nodes.values())
    rows = []
    for node, comp_type in gr_nodes.items():
        base, pos = parse_gr_node(node)
        rows.append((comp_type, base, pos, node))
    rows.sort(key=lambda x: (x[0], x[1], x[2]))
    keep, taken = set(), Counter()
    for t, base, pos, node in rows:
        need = demand.get(t, 0)
        if need <= 0: continue
        if taken[t] < need:
            keep.add(node); taken[t] += 1
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
    if len(parts) == 2: return parts[0]
    if len(parts) == 3: return ".".join(parts[:2])
    return name

def _build_lookup(min_edges):
    return {
        tuple(e["edge"].strip("()").replace("'", "").split(", ")): e["distance"]
        for e in min_edges
    }

def _get_distance(src, dst, lookup, default=10**9):
    if (src, dst) in lookup: return lookup[(src, dst)]
    bs, bd = _get_base(src), _get_base(dst)
    for (s, d), w in lookup.items():
        if _get_base(s) == bs and d == dst:
            return w
    for (s, d), w in lookup.items():
        if s == src and _get_base(d) == bd:
            return w
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
    require_type_match_gr_kh=False  # RELAXED for simulation, too
):
    lookup = _build_lookup(min_edges)
    BIG = 10**8
    out = []

    gr_set = set(gr_nodes.keys())
    kh_set = set(kh_nodes.keys())

    # 0.0 -> GR (only *.1)
    for g in gr_set:
        r, c, i = _parse_gr(g)
        if i != "1": continue
        w = _get_distance("0.0", g, lookup)
        if w < BIG: out.append({"edge": f"(0.0, {g})", "distance": w + add_bias})

    # GR -> KH (relaxed)
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
            if w < BIG: out.append({"edge": f"({kh}, {g})", "distance": w + add_bias})

    # KH -> 0.0.0
    for kh in kh_set:
        w = _get_distance(kh, "0.0.0", lookup)
        if w < BIG: out.append({"edge": f"({kh}, 0.0.0)", "distance": w + add_bias})

    # 0.0.0 -> 0.0
    w = _get_distance("0.0.0", "0.0", lookup)
    if w < BIG: out.append({"edge": "(0.0.0, 0.0)", "distance": w})

    # KH -> KH (no self)
    kh_faces = list(kh_set)
    for u in kh_faces:
        for v in kh_faces:
            if u == v: continue
            w = _get_distance(u, v, lookup)
            if w < BIG: out.append({"edge": f"({u}, {v})", "distance": w})

    # GR -> GR next-index same-base
    by_base = defaultdict(set)
    for g in gr_set:
        r, c, i = _parse_gr(g)
        if r is None: continue
        by_base[f"{r}.{c}"].add(int(i))
    for base, idxs in by_base.items():
        for k in sorted(idxs):
            nxt = k + 1
            if nxt in idxs:
                u = f"{base}.{k}"
                v = f"{base}.{nxt}"
                w = _get_distance(u, v, lookup)
                if w < BIG: out.append({"edge": f"({u}, {v})", "distance": w})

    # cross-rack GR→GR
    if allow_cross_rack_gr_pick2:
        gl = list(gr_set)
        for u in gl:
            ru, cu, iu = _parse_gr(u)
            if ru is None: continue
            for v in gl:
                if u == v: continue
                rv, cv, iv = _parse_gr(v)
                if rv is None: continue
                if (ru, cu) == (rv, cv): continue
                w = _get_distance(u, v, lookup)
                if w < BIG: out.append({"edge": f"({u}, {v})", "distance": w + cross_gr_extra_bias})

    # strip self loops
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
    return sum(int(G[tour[i]][tour[i+1]]["weight"]) for i in range(len(tour)-1))

def shuffle_gr_sequence(original_seq, *, rng):
    """Return a new gr_sequence with containers permuted across positions."""
    # flatten
    positions, containers = [], []
    for d in original_seq:
        [(pos, cid)] = d.items()
        positions.append(pos)
        containers.append(cid)
    perm = containers[:]
    rng.shuffle(perm)
    return [{pos: cid} for pos, cid in zip(positions, perm)]


def main():
    # -------- load input --------
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = INPUT_PATH

    with open(path) as f:
        msg = json.load(f)
    base_data = msg.get("data", msg)

    rng = random.Random(SEED)

    # ========== BASELINE on current GR sequence ==========
    edges, gr_types, kh_types = build_edges_from_input(
        base_data, use_prune=USE_PRUNE, require_type_match_gr_kh=False
    )
    a2b = create_distance_matrices({"data": {"distance_matrix": edges}})

    templates = base_data.get("templates", {})
    kit_holders_tpl = templates.get("kit_holders_opt", base_data.get("kit_holders_opt", {}))
    kh_seq = templates.get("kh_sequences_opt", base_data.get("kh_sequences_opt", []))
    kh_nodes_again = generate_kh_nodes(kh_seq, kit_holders_tpl)
    active_kh_nodes = sorted(kh_nodes_again.keys())

    missing = [n for n in active_kh_nodes if n not in a2b.index or n not in a2b.columns]
    if missing:
        raise ValueError(f"KH nodes not in matrix: {missing}")

    B, set_1, set_2 = create_directed_bipartite_graph(a2b, active_kh_nodes)

    start_node, end_node = "0.0", "0.0.0"

    tour_h = nearest_tsp_dual(B, start_node, end_node, set_1, set_2, gr_types, kh_types, max_load=2, verbose=False)
    cost_h = compute_path_cost(B, tour_h)

    lin = linear_picking_dual(B, start_node, end_node, set_1, set_2, gr_types, kh_types, filtered_matrix=edges)
    tour_l = lin["tour"]; cost_l = lin.get("total_cost", compute_path_cost(B, tour_l))

    baseline = {
        "dual_heuristic": {"cost": str(cost_h)},
        "dual_linear": {"cost": str(cost_l)},
        "gr_sequence": base_data["gr_sequence"]
    }

    # ========== SEARCH over shuffled GR layouts ==========
    best = {
        "phase": 0,
        "dual_heuristic_cost": str(cost_h),
        "improvement_heuristic": 0.0,
        "improvement_linear": 0.0,
        "gr_sequence": base_data["gr_sequence"]
    }

    t0 = int(time() * 1000)

    for phase in range(1, N_PHASES + 1):
        trial_data = deepcopy(base_data)
        trial_data["gr_sequence"] = shuffle_gr_sequence(base_data["gr_sequence"], rng=rng)

        # rebuild edges/graph per layout
        edges_t, gr_t, kh_t = build_edges_from_input(trial_data, use_prune=USE_PRUNE, require_type_match_gr_kh=False)
        a2b_t = create_distance_matrices({"data": {"distance_matrix": edges_t}})
        B_t, set_1_t, set_2_t = create_directed_bipartite_graph(a2b_t, active_kh_nodes)

        # heuristic
        th = nearest_tsp_dual(B_t, start_node, end_node, set_1_t, set_2_t, gr_t, kh_t, max_load=2, verbose=False)
        ch = compute_path_cost(B_t, th)

        # linear
        lin_t = linear_picking_dual(B_t, start_node, end_node, set_1_t, set_2_t, gr_t, kh_t, filtered_matrix=edges_t)
        tl = lin_t["tour"]; cl = lin_t.get("total_cost", compute_path_cost(B_t, tl))

        # improvements vs BASELINE, keep if better on heuristic
        imp_h = round(((int(baseline["dual_heuristic"]["cost"]) - ch) / int(baseline["dual_heuristic"]["cost"])) * 100, 4)
        imp_l = round(((int(baseline["dual_linear"]["cost"])       - cl) / int(baseline["dual_linear"]["cost"])) * 100, 4)

        if ch < int(best["dual_heuristic_cost"]):
            best = {
                "phase": phase,
                "dual_heuristic_cost": str(ch),
                "improvement_heuristic": imp_h,
                "improvement_linear": imp_l,
                "gr_sequence": trial_data["gr_sequence"]
            }

    out = {
        "simulation_run": True,
        "message": "Simulation completed.",
        "baseline": baseline,
        "best_phase": best,
        "solutionTime": (int(time() * 1000) - t0),
        "totalTime": (int(time() * 1000) - t0)
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(out, f, indent=2)
    print(f"✅ Wrote {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
