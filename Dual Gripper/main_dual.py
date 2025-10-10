# main_dual.py — run heuristic AND linear on a RELAXED GR→KH graph (for comparison)
import json
import sys
from collections import defaultdict, Counter
from time import time

from parse_json_dual import create_distance_matrices
from GraphCreation_dual import create_directed_bipartite_graph
from dual_gripper_heuristic import nearest_tsp_dual
from linear_dual import linear_picking_dual

# ====== CONFIG ======
DEFAULT_JSON = "input_dual_gripper.json"
ADD_EDGE_BIAS = 2000
ALLOW_CROSS_RACK_GR_PICK2 = True     # allow GR→GR across different bases (pick→pick)
CROSS_GR_EXTRA_BIAS = 0              # penalty for cross-rack GR→GR hops
USE_PRUNE = True                     # prune GR pockets to exactly KH demand
OUTPUT_PATH = "output_dual_relaxed.json"

# RELAX GR→KH type matching for this experiment (connect ALL GR->KH pairs)
REQUIRE_TYPE_MATCH_GR_KH = False

ALLOWED_METHODS = {"dual_heuristic", "linear_dual", "dual-linear"}
# ====================


# ---------- helpers (copied from main, trimmed) ----------
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
                        kh_nodes[f"{kh_pos}.{comp['position']}"] = comp["type"]
    return kh_nodes

def generate_gr_nodes(gr_sequence, container_types):
    gr_nodes = {}
    for entry in gr_sequence:
        for gr_pos, container_id in entry.items():
            if container_id in container_types:
                for comp in container_types[container_id].get("contents", []):
                    if isinstance(comp, dict) and "position" in comp and "type" in comp:
                        gr_nodes[f"{gr_pos}.{comp['position']}"] = comp["type"]
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
    if (src, dst) in lookup:
        return lookup[(src, dst)]
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
        require_type_match_gr_kh=REQUIRE_TYPE_MATCH_GR_KH,  # RELAXED here
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

    # GR -> KH (RELAXED: connect all GR->KH)
    for g, t in gr_nodes.items():
        for kh, kt in kh_nodes.items():
            if require_type_match_gr_kh and t != kt:
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

    # KH -> 0.0.0 and 0.0.0 -> 0.0
    for kh in kh_set:
        w = _get_distance(kh, "0.0.0", lookup)
        if w < BIG:
            out.append({"edge": f"({kh}, 0.0.0)", "distance": w + add_bias})
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

    # GR -> GR (same base +1) and cross-rack if enabled
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
                    continue  # same-base handled above
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

def build_edges_from_input(
    data,
    use_prune=USE_PRUNE,
    require_type_match_gr_kh=REQUIRE_TYPE_MATCH_GR_KH
):
    templates = data.get("templates", {})
    containers = templates.get("containers_opt", data.get("containers_opt", {}))
    kit_holders = templates.get("kit_holders_opt", data.get("kit_holders_opt", {}))
    kh_sequences_opt = templates.get("kh_sequences_opt", data.get("kh_sequences_opt", []))
    min_edges = data.get("distance_matrix_min", templates.get("distance_matrix_min", []))

    gr_nodes_full = generate_gr_nodes(data["gr_sequence"], containers)
    kh_nodes = generate_kh_nodes(kh_sequences_opt, kit_holders)

    gr_nodes = prune_gr_nodes_to_demand(gr_nodes_full, kh_nodes) if use_prune else gr_nodes_full
    if use_prune:
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

def check_rules(
    edges,
    gr_nodes,
    kh_nodes,
    allow_cross_rack_gr_pick2=ALLOW_CROSS_RACK_GR_PICK2,
    require_type_match_gr_kh=REQUIRE_TYPE_MATCH_GR_KH,
):
    gr_set = set(gr_nodes.keys())
    kh_set = set(kh_nodes.keys())

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

    # GR -> GR step rule
    for e in edges:
        s, d = parse_edge(e)
        if s in gr_set and d in gr_set:
            rb, cb, i1 = _parse_gr(s)
            ra, ca, i2 = _parse_gr(d)
            if allow_cross_rack_gr_pick2:
                if (rb, cb) == (ra, ca) and int(i2) != int(i1) + 1:
                    violations.append(f"GR→GR wrong step (same-base must be +1): {s} -> {d}")
            else:
                if (rb, cb) != (ra, ca) or int(i2) != int(i1) + 1:
                    violations.append(f"GR→GR wrong step: {s} -> {d}")

    # require 0.0.0 -> 0.0
    if not any(e["edge"] == "(0.0.0, 0.0)" for e in edges):
        violations.append("Missing required edge: (0.0.0, 0.0)")

    return violations

def edge_weight(G, u, v):
    return int(G[u][v]["weight"])

def node_kind(node, gr_types, kh_types):
    if node in gr_types:
        return "GR"
    if node in kh_types:
        return "KH"
    if node in ("0.0", "0.0.0"):
        return "HOME"
    return "OTHER"

def build_time_details_from_tour(G, tour, gr_types, kh_types):
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

def compute_path_cost(G, tour):
    cost = 0
    for u, v in zip(tour, tour[1:]):
        if not G.has_edge(u, v):
            raise ValueError(f"No edge {u} -> {v} in graph.")
        cost += int(G[u][v]["weight"])
    return cost


# ---------- runner (RELAXED graph; supports both methods + comparison) ----------
def run_dual_relaxed(json_file_path=None, input_data=None):
    """
    Run dual-gripper on a RELAXED GR→KH graph (all GR->KH pairs allowed):
      - method == "dual_heuristic": heuristic only
      - method == "linear_dual":    linear baseline only
      - method == "dual-linear":    run both and report the better + improvement %
    """
    t0_solution = int(time() * 1000)
    t0_total = int(time() * 1000)

    if input_data and "data" in input_data:
        data = input_data["data"]
    elif json_file_path:
        with open(json_file_path) as f:
            msg = json.load(f)
        data = msg.get("data", msg)
    else:
        raise ValueError("run_dual_relaxed needs either json_file_path or input_data")

    method = data.get("method", "dual_heuristic")
    if method not in ALLOWED_METHODS:
        raise ValueError(f"Unknown method '{method}'. Allowed: {sorted(ALLOWED_METHODS)}")

    # Build relaxed graph ONCE (used by both methods here)
    edges, gr_nodes, kh_nodes = build_edges_from_input(
        data,
        use_prune=USE_PRUNE,
        require_type_match_gr_kh=False,  # RELAXED
    )

    # Optional rule check (doesn't check GR→KH types because we relaxed it)
    violations = check_rules(
        edges, gr_nodes, kh_nodes,
        allow_cross_rack_gr_pick2=ALLOW_CROSS_RACK_GR_PICK2,
        require_type_match_gr_kh=False,
    )
    if violations:
        print("⚠️ RULE CHECKS (relaxed) — non-fatal:")
        for v in violations[:50]:
            print("  -", v)
        if len(violations) > 50:
            print(f"  ... and {len(violations)-50} more")

    # Build matrix & graph
    a_to_b_matrix = create_distance_matrices({"data": {"distance_matrix": edges}})

    # Active KH axis
    templates = data.get("templates", {})
    kit_holders_tpl = templates.get("kit_holders_opt", data.get("kit_holders_opt", {}))
    kh_seq = templates.get("kh_sequences_opt", data.get("kh_sequences_opt", []))
    kh_nodes_again = generate_kh_nodes(kh_seq, kit_holders_tpl)
    active_kh_nodes = sorted(kh_nodes_again.keys())

    missing = [n for n in active_kh_nodes if n not in a_to_b_matrix.index or n not in a_to_b_matrix.columns]
    if missing:
        raise ValueError(f"KH nodes not in matrix: {missing}")

    B, set_kh, set_gr = create_directed_bipartite_graph(a_to_b_matrix, active_kh_nodes)

    start_node = "0.0"
    end_node = "0.0.0"

    results = {}

    # Heuristic branch
    if method in ("dual_heuristic", "dual-linear"):
        tour_h = nearest_tsp_dual(
            G=B,
            start=start_node,
            end=end_node,
            set_kh=set_kh,
            set_gr=set_gr,
            gr_types=gr_nodes,
            kh_types=kh_nodes,
            max_load=2,
            verbose=False
        )
        cost_h = compute_path_cost(B, tour_h)
        time_h = build_time_details_from_tour(B, tour_h, gr_nodes, kh_nodes)
        results["dual_heuristic_relaxed"] = {"cost": cost_h, "tour": tour_h, "time_details": time_h}

    # Linear baseline branch
    if method in ("linear_dual", "dual-linear"):
        lin = linear_picking_dual(
            B=B,
            start_node=start_node,
            end_node=end_node,
            set_kh=set_kh,
            set_gr=set_gr,
            gr_types=gr_nodes,
            kh_types=kh_nodes,
            filtered_matrix=edges  # if your linear uses explicit weights dict
        )
        tour_l = lin["tour"]
        cost_l = lin.get("total_cost", compute_path_cost(B, tour_l))
        time_l = build_time_details_from_tour(B, tour_l, gr_nodes, kh_nodes)
        results["linear_dual_relaxed"] = {"cost": cost_l, "tour": tour_l, "time_details": time_l}

    # Compare (like exact-linear)
    if method == "dual-linear":
        if ("dual_heuristic_relaxed" in results) and ("linear_dual_relaxed" in results):
            c_h = results["dual_heuristic_relaxed"]["cost"]
            c_l = results["linear_dual_relaxed"]["cost"]
            improvement = round(((c_l - c_h) / c_l) * 100, 4) if c_l else 0.0
            if improvement > 0:
                results = {
                    "dual_heuristic_relaxed": results["dual_heuristic_relaxed"],
                    "improvement_percentage": improvement
                }
            else:
                results = {
                    "linear_dual_relaxed": results["linear_dual_relaxed"],
                    "improvement_percentage": improvement
                }

    output_data = {
        "optimization_run": True,
        "message": f"Ran method '{method}' on RELAXED graph successfully.",
        "solutionTime": (int(time() * 1000) - t0_solution),
        "totalTime": (int(time() * 1000) - t0_total),
        "optimization_results": results
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output_data, f, indent=2)
    print(f"✅ Wrote {OUTPUT_PATH}")

    return output_data


if __name__ == "__main__":
    path = DEFAULT_JSON if len(sys.argv) < 2 else sys.argv[1]
    run_dual_relaxed(json_file_path=path)
