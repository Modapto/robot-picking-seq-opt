from flask import Flask, request, jsonify

app = Flask(__name__)

# global variable to store kh_sequence
kh_sequence = {}

def translate_kh_sequences_sim(kh_sequences_sim):
    translated = []
    for phase in kh_sequences_sim:
        phase_sequence = []
        for d in phase:
            for _, v in d.items():
                phase_sequence.append(v)
        translated.append(phase_sequence)
    return translated

@app.route('/simulation', methods=['POST'])
def receive_kh_sequences():
    global kh_sequence
    try:
        data = request.get_json()
        kh_sequences_sim = data["data"]["templates"]["kh_sequences_sim"]
        kh_sequence = kh_sequences_sim
        translated = translate_kh_sequences_sim(kh_sequences_sim)
        return jsonify({"kh_sequences": translated})
    except Exception as e:
        return jsonify({"error!": str(e)}), 400

@app.route('/simulation', methods=['GET'])
def return_kh_sequences():
    global kh_sequence
    if not kh_sequence:
        return jsonify({"error!": "No KH sequence posted yet."}), 404
    translated = translate_kh_sequences_sim(kh_sequence)
    return jsonify({"kh_sequences": translated})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81)