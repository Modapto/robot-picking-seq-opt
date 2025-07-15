from flask import Flask, request, jsonify
import json

app = Flask(__name__)

def translate_kh_sequences_sim(kh_sequences_sim):
    translated = []
    for phase in kh_sequences_sim:
        phase_sequence = []
        for d in phase:
            for _, v in d.items():
                phase_sequence.append(v)
        translated.append(phase_sequence)
    return translated

# @app.route('/simulation',methods=['POST'])
# def simulation():
#     try:
#         data = request.get_json()
#         kh_sequences_sim = data["data"]["templates"]["kh_sequences_sim"]
#         translated = translate_kh_sequences_sim(kh_sequences_sim)
#         return jsonify({"kh_sequences": translated})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 400
#
# app.run(host='0.0.0.0', port=81)

@app.route('/simulation',methods=['GET', 'POST'])
def simulation():
    if request.method == "POST":
        data = request.get_json()
        kh_sequences_sim = data["data"]["templates"]["kh_sequences_sim"]
    else:
        # for GET test — fallback to default local file
        with open("co_pilot_execution_input.json") as f:
            input_data = json.load(f)
        kh_sequences_sim = input_data["data"]["templates"]["kh_sequences_sim"]

    translated = translate_kh_sequences_sim(kh_sequences_sim)
    return {"kh_sequences": translated}

app.run(host='0.0.0.0', port=81)