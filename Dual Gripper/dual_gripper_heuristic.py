import math
from collections import Counter

def nearest_tsp_dual(
    G,
    start: str,
    end: str,
    set_kh: list,
    set_gr: list,
    gr_types: dict,   # e.g., {'1.1.1':'Component_5', ...}
    kh_types: dict,   # e.g., {'1.1':'Component_5', ...}
    max_load: int = 2,
    large_value: float = 1e12,
    verbose: bool = True
):
    """
    Simple nearest-neighbor heuristic for dual-gripper.
    - Allows GR→GR and KH→KH moves (whatever edges your graph provides).
    - Won't visit `end` until all KH nodes are visited.
    - Tracks an in-hand buffer (<= max_load) by component type to prefer sensible GR picks / KH placements.

    Returns:
        tour: list[str]
    """

    # --- helpers ---
    def edge_w(u, v):
        if G.has_edge(u, v):
            return G[u][v].get('weight', large_value)
        return large_value

    def nearest(current, candidates):
        best = None
        best_w = large_value
        for c in candidates:
            if c == current:      # no self transitions
                continue
            w = edge_w(current, c)
            if w < best_w:
                best_w = w
                best = c
        return best, best_w

    # remaining KH demand by type (unvisited KH slots)
    rem_kh_by_type = Counter(kh_types.values())

    visited = {n: False for n in G.nodes}
    # keep `end` unvisited until the end by design
    for n in [start, end]:
        if n in visited:
            visited[n] = False

    tour = [start]
    current = start
    visited[start] = True

    # a small "hand" inventory: type -> count up to max_load
    in_hand = Counter()

    # sets as sets for faster ops
    KH = set(set_kh)
    GR = set(set_gr)

    # convenience lists
    KH_unv = set([n for n in set_kh if not visited.get(n, False)])
    GR_unv = set([n for n in set_gr if not visited.get(n, False)])

    def can_pick(gr_node):
        """We pick from GR only if we have capacity and that type is still needed by any KH."""
        if len(list(in_hand.elements())) >= max_load:
            return False
        t = gr_types.get(gr_node, None)
        return t is not None and rem_kh_by_type[t] > 0

    def can_place(kh_node):
        """We place to KH only if KH not visited and we hold its type."""
        if visited.get(kh_node, False):
            return False
        t = kh_types.get(kh_node, None)
        return t is not None and in_hand[t] > 0

    def all_kh_done():
        return all(visited.get(k, False) for k in KH)

    if verbose:
        print(f"[dual-NN] start={start}, end={end}, |KH|={len(KH)}, |GR|={len(GR)}")

    # --- main loop ---
    while not all_kh_done():
        # 1) If we can place, prefer nearest placeable KH from current
        placeable = [k for k in KH_unv if can_place(k) and G.has_edge(current, k)]
        next_node, next_w = nearest(current, placeable) if placeable else (None, large_value)

        # 2) Else, if we have capacity, prefer nearest useful GR (whose type is still needed)
        if next_node is None and len(list(in_hand.elements())) < max_load:
            pickable = [g for g in GR_unv if can_pick(g) and G.has_edge(current, g)]
            next_node, next_w = nearest(current, pickable) if pickable else (None, large_value)

        # 3) Else, pure NN among any unvisited legal neighbors except `end`
        if next_node is None:
            neighs = [v for v in G.successors(current)
                      if not visited.get(v, False)
                      and v != end]  # don't go to end yet
            next_node, next_w = nearest(current, neighs)

        if next_node is None:
            raise ValueError(f"No valid neighbor from {current}. Tour may be stuck.")

        # apply move
        tour.append(next_node)
        visited[next_node] = True
        if next_node in KH_unv:
            KH_unv.remove(next_node)
        if next_node in GR_unv:
            GR_unv.remove(next_node)

        # update in-hand / remaining demand
        if next_node in GR:
            t = gr_types.get(next_node, None)
            if t is not None and len(list(in_hand.elements())) < max_load and rem_kh_by_type[t] > 0:
                in_hand[t] += 1
                if verbose:
                    print(f" pick {next_node} (type {t}), in_hand={dict(in_hand)}")
        elif next_node in KH:
            t = kh_types.get(next_node, None)
            if t is not None and in_hand[t] > 0:
                in_hand[t] -= 1
                rem_kh_by_type[t] -= 1
                if verbose:
                    print(f" place {next_node} (type {t}), in_hand={dict(in_hand)}, rem_kh={dict(rem_kh_by_type)}")

        if verbose:
            print(f"  → {current} -> {next_node} (w={next_w})")
        current = next_node

    # when all KH visited, go to end if possible, then back to start if exists
    if current != end:
        if G.has_edge(current, end):
            tour.append(end)
            if verbose:
                print(f"done with KH. going {current} -> {end}")
        else:
            # nearest hop chain to reach end (fallback)
            neighs = [v for v in G.successors(current) if not (v == current)]
            nxt, _ = nearest(current, neighs)
            if nxt is None:
                raise ValueError(f"Cannot reach {end} from {current}.")
            tour.append(nxt)
            current = nxt
            if G.has_edge(current, end):
                tour.append(end)

    # return to 0.0 if that edge exists (your graph usually has 0.0.0 -> 0.0)
    if G.has_edge(end, start):
        tour.append(start)
        if verbose:
            print(f"return {end} -> {start}")

    return tour


def total_cost(G, tour):
    cost = 0
    time_details = []
    for i in range(len(tour) - 1):
        u, v = tour[i], tour[i + 1]
        if G.has_edge(u, v):
            w = G[u][v].get('weight', math.inf)
            cost += w
            time_details.append({"from": u, "to": v, "totalTime": w})
        else:
            # unreachable step (shouldn't happen if graph was respected)
            time_details.append({"from": u, "to": v, "totalTime": math.inf, "note": "no edge"})
    return cost, time_details
