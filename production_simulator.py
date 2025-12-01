# REPOSITORY NAME (c) by the University of Piraues, Greece.
#
# REPOSITORY NAME is licensed under a
# Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <http://creativecommons.org/licenses/by-nc-nd/3.0/>.

from flask import Flask, request, jsonify

app = Flask(__name__)

# global variable to store kh_sequence
kh_sequence = {}

def translate_kh_sequences_sim(kh_sequences_sim):
    """
    Translate KH sequences from dict-based format to list-of-lists.

    Input format example:
        [
          [ {"1": "KH001"}, {"2": "KH003"} ],
          [ {"1": "KH002"}, {"2": "KH001"} ]
        ]

    Output format:
        [
          ["KH001", "KH003"],
          ["KH002", "KH001"]
        ]
    """
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
    """
    Receive KH sequences via POST and store them in a global variable.

    Expected JSON body structure:
        {
          "data": {
            "templates": {
              "kh_sequences_sim": [ ... ]
            }
          }
        }

    The endpoint:
        - Extracts "kh_sequences_sim",
        - Stores it in the global `kh_sequence`,
        - Returns the translated list-of-lists format.

    """
    global kh_sequence
    try:
        data = request.get_json()
        kh_sequences_sim = data["data"]["templates"]["kh_sequences_sim"]
        kh_sequence = kh_sequences_sim
        translated = translate_kh_sequences_sim(kh_sequences_sim)
        return jsonify({"kh_sequences": translated})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/simulation', methods=['GET'])
def return_kh_sequences():
    """
    Return the last posted KH sequences in translated form.

    If no sequences have been posted yet, it returns a 404 error.
    """
    global kh_sequence
    if not kh_sequence:
        return jsonify({"error!": "No KH sequence posted yet."}), 404
    translated = translate_kh_sequences_sim(kh_sequence)
    return jsonify({"kh_sequences": translated})

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=10101)