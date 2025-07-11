# kh_simulation.py

def translate_kh_sequences_sim(kh_sequences_sim):
    """
    Convert input like:
        [[{"1": "KH001"}, {"2": "KH002"}], ...]
    Into:
        [["KH001", "KH002"], ...]
    """
    translated = []
    for phase in kh_sequences_sim:
        phase_sequence = []
        for d in phase:
            for _, v in d.items():
                phase_sequence.append(v)
        translated.append(phase_sequence)
    return translated
