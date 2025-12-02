# REPOSITORY NAME (c) by the University of Piraues, Greece.
#
# REPOSITORY NAME is licensed under a
# Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <http://creativecommons.org/licenses/by-nc-nd/3.0/>.

import requests
import json
import base64
import pickle

# load encoded input
with open("co_encoded_input.json") as f:
    input_data = json.load(f)

# decode base64
if "base64" in input_data["data"]:
    raw = base64.b64decode(input_data["data"]["base64"])
    try:
        input_data["data"] = pickle.loads(raw)
    except pickle.UnpicklingError:
        input_data["data"] = json.loads(raw.decode())


resp = requests.post('http://localhost:81/simulation', json={"data": input_data["data"]})
print("STATUS:", resp.status_code)
print("RESPONSE TEXT:", resp.text)

print(resp.json())