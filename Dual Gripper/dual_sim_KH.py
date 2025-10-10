# dual_sim_KH.py
import copy

def normalize_kh_sequences(kh_sequences):
    """
    Keep KH sequences in the same normalized list[dict] shape:
      e.g. [{"1": "KH_A"}, {"2": "KH_B"}, ...] or [{"1": "kit1"}, ...].
    This function is a no-op normalizer so simulation stays flexible if
    later you want to permute KHs as well.
    """
    if isinstance(kh_sequences, list):
        return kh_sequences[:]
    if isinstance(kh_sequences, dict):
        return [{k: v} for k, v in kh_sequences.items()]
    return []

def apply_kh_sequences_to_data(data, new_kh_sequences):
    """
    Deep-copy data and swap 'kh_sequences_opt' if present (dual project uses
    templates.kh_sequences_opt). If yours is at top-level 'kh_sequences',
    feel free to mirror the assignment.
    """
    new_data = copy.deepcopy(data)
    # Try both common locations used in the dual project
    if "templates" in new_data:
        new_data["templates"] = copy.deepcopy(new_data["templates"])
        new_data["templates"]["kh_sequences_opt"] = normalize_kh_sequences(new_kh_sequences)
    else:
        new_data["kh_sequences_opt"] = normalize_kh_sequences(new_kh_sequences)
    return new_data
