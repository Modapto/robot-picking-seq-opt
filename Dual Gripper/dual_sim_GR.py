# dual_sim_GR.py
import copy
import random

def normalize_gr_sequence(gr_sequence):
    """
    Input can be:
      - list[ dict[str, str] ] like [{"1.1": "Container_A"}, ...]
      - dict[str, str] like {"1.1": "Container_A", ...}
    Returns a *list* of single-key dicts sorted by numeric row/col for stability.
    """
    if isinstance(gr_sequence, dict):
        items = list(gr_sequence.items())
    else:
        items = []
        for entry in gr_sequence:
            items.extend(entry.items())

    def rc_key(pos):
        try:
            r, c = pos.split(".")
            return (int(r), int(c))
        except Exception:
            return (10**9, pos)

    items.sort(key=lambda kv: rc_key(kv[0]))
    return [{k: v} for k, v in items]

def extract_positions_and_containers(gr_sequence):
    norm = normalize_gr_sequence(gr_sequence)
    positions = [list(d.keys())[0] for d in norm]
    containers = [list(d.values())[0] for d in norm]
    return positions, containers

def shuffle_container_positions(gr_sequence, seed=None, strategy="shuffle"):
    """
    Produce a *new* GR sequence by reassigning containers to positions.
    Strategies:
      - "shuffle"      : full random permutation
      - "swap_pairs"   : a handful of random pair swaps (milder)
      - "block_rotate" : rotate each row's containers by one position
    """
    rng = random.Random(seed)
    positions, containers = extract_positions_and_containers(gr_sequence)
    new_containers = containers[:]

    if strategy == "shuffle":
        rng.shuffle(new_containers)

    elif strategy == "swap_pairs":
        swaps = max(1, len(new_containers) // 5)
        for _ in range(swaps):
            i = rng.randrange(len(new_containers))
            j = rng.randrange(len(new_containers))
            new_containers[i], new_containers[j] = new_containers[j], new_containers[i]

    elif strategy == "block_rotate":
        # rotate within each row (1.x together, 2.x together, etc.)
        rows = {}
        for idx, pos in enumerate(positions):
            try:
                r, c = pos.split(".")
                rows.setdefault(int(r), []).append((int(c), idx))
            except Exception:
                rows.setdefault(0, []).append((idx, idx))

        out = new_containers[:]
        for r, lst in rows.items():
            lst.sort()  # by column
            idxs = [j for _, j in lst]
            if not idxs:
                continue
            first = out[idxs[0]]
            for k in range(len(idxs) - 1):
                out[idxs[k]] = out[idxs[k + 1]]
            out[idxs[-1]] = first
        new_containers = out

    else:
        # default to random shuffle for unknown strategy
        rng.shuffle(new_containers)

    return [{pos: cont} for pos, cont in zip(positions, new_containers)]

def apply_gr_sequence_to_data(data, new_gr_sequence):
    """
    Return a deep-copied data payload with 'gr_sequence' replaced.
    (Does not alter templates, distances, etc.)
    """
    new_data = copy.deepcopy(data)
    new_data["gr_sequence"] = normalize_gr_sequence(new_gr_sequence)
    return new_data
