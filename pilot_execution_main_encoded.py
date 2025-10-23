import json, sys, copy, traceback, base64, pickle
from datetime import datetime
from time import time
import pika
from pilot_co_sim_execution import run_simulation
from pilot_opt_execution import run_tsp
from mqtt_integration import publish_message
from pilot_production_simulator import app
import requests
import threading

class thread(threading.Thread):
    def __init__(self, thread_name, thread_ID):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_ID = thread_ID

        # helper function to execute the threads
    def run(self):
        app.run(host='0.0.0.0', port=10101);

# ───────────────────── helper: decode & inject templates ─────────────────────
def decode_data_block(msg: dict) -> None:
    """
    Replace msg['data'] in-place with a plain dict.
    Handles:
        {'base64': <pickle>}  →  pickle.loads
        {'base64': <json>}    →  json.loads
        { ... }               →  already plain
    """
    if isinstance(msg.get("data"), dict) and "base64" in msg["data"]:
        raw = base64.b64decode(msg["data"]["base64"])
        try:
            msg["data"] = pickle.loads(raw)
        except pickle.UnpicklingError:
            msg["data"] = json.loads(raw.decode())

def inject_templates(msg: dict) -> None:
    decode_data_block(msg)                 # ensure plain dict first
    data      = msg["data"]
    templates = data.get("templates")
    if templates is None:
        raise ValueError("Missing 'templates' block")

    method = data["method"].lower()
    if method == "simulation":
        data["containers_template"]  = templates["containers_sim"]
        data["kit_holders_template"] = templates["kit_holders_sim"]
        data["distance_matrix"]      = templates["distance_matrix_sim"]
        resp = requests.post('http://localhost:10101/simulation', json={"data": data})
        print("FLASK RESPONSE STATUS:", resp.status_code)
        print("FLASK RAW TEXT:", resp.text)
        data["kh_sequences"] = resp.json()["kh_sequences"]
    elif method in {"exact", "linear", "exact-linear"}:
        data["containers_template"]  = templates["containers_opt"]
        data["kit_holders_template"] = templates["kit_holders_opt"]
        data["distance_matrix"]      = templates["distance_matrix_opt"]
        data["kh_sequences"]         = templates["kh_sequences_opt"]
    else:
        raise ValueError(f"Unknown method '{method}' ")


# ───────────────────────── RabbitMQ callback ─────────────────────────
def callback(ch, method, properties, body):
    input_file = json.loads(body)
    uuid = input_file.get('uuid', 'unknown')
    try:
        print(f"{datetime.now():%d/%m/%Y %H:%M:%S}: Job {uuid} received")
        inject_templates(input_file)              # decode & splice once
        print("1. Input decoded")
        data = input_file["data"]
        print(data)
        pilot = 'CRF'
        priority = "HIGH"
        production_module = data['module']
        smart_service = data['smartService']
        print("2. Required fields mapped")

        if data["method"] == "simulation":
            print("3. Starting simulation")
            result = run_simulation(input_file)
            print("4. Finished simulation")
            source_component = 'Robot picking sequence simulation method'
            description = 'Completion of simulation algorithm'
            event_type = 'Simulation Completion'
            topic = 'kh-picking-sequence-simulation'
        else:
            print("3. Starting optimization")
            result = run_tsp(None, input_file, False)
            print("4. Finished optimization")
            source_component = 'Robot picking sequence optimization method'
            description = 'Completion of optimization algorithm'
            event_type = 'Optimization Completion'
            topic = 'kh-picking-sequence-optimization'

        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        print("5. MQTT publishing")
        publish_message(mqtt_broker, mqtt_port, mqtt_auth, description,
                        production_module, pilot, timestamp, priority, event_type,
                        source_component, smart_service, topic, result)

        output = {
            "uuid": uuid,
            "produced_at": int(time() * 1000),
            "data": {
                "base64": base64.b64encode(pickle.dumps(result)).decode()
            }
        }
        print("6. Rabbit publishing")
        ch.basic_publish(exchange='opt-result',
                         routing_key='robot-picking-seq',
                         body=json.dumps(output))
        print(f"{datetime.now():%d/%m/%Y %H:%M:%S}: Job {uuid} completed")

    except Exception as exc:
        traceback.print_exc()
        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        error = {"message": f"Problem in input data: {exc}"}
        print("5. EXCEPTION: MQTT publishing")
        publish_message(mqtt_broker, mqtt_port, mqtt_auth, 'Error in Simulation/Optimization service',
                        production_module, pilot, timestamp, priority, 'Error',
                        source_component, smart_service, topic, error)
        error_responce = {
            "uuid": uuid,
            "produced_at": int(time() * 1000),
            "data": {
                "base64": base64.b64encode(
                    pickle.dumps({"message": f"Problem in input data: {exc}"})
                ).decode()
            }
        }
        print("6. EXCEPTION: Rabbit publishing")
        ch.basic_publish(exchange='opt-result',
                         routing_key='robot-picking-seq',
                         body=json.dumps(error_responce))
        print(f"{datetime.now():%d/%m/%Y %H:%M:%S}: Job {uuid} failed")


online = sys.argv[1]
mqtt_broker = ''
mqtt_port = 0
mqtt_auth = {'username': '', 'password': ''}
mqtt_topic = ''

prodSim = thread("productionSimulator", 1000)
prodSim.daemon = True
prodSim.start()

if online == "1":
    host, port, user, pw, mqtt_broker, mqtt_port, mqtt_username, mqtt_pw = sys.argv[2:11]
    mqtt_port = int(mqtt_port)
    mqtt_auth = {'username': mqtt_username, 'password': mqtt_pw}
    conn = pika.BlockingConnection(pika.ConnectionParameters(
        host, int(port), '/', pika.PlainCredentials(user, pw),
        heartbeat=1800, blocked_connection_timeout=900))
    channel = conn.channel()
    channel.basic_consume(queue='robot-picking-seq_job',
                          auto_ack=True,
                          on_message_callback=callback)
    print(" [*] Waiting for messages.")
    channel.start_consuming()

elif online == "0":
    filename = sys.argv[2]
    with open(filename) as f:
        local_msg = json.load(f)

    inject_templates(local_msg)            # decode & splice once
    data = local_msg["data"]

    if data["method"] == "simulation":
        print("Running simulation locally …")
        run_simulation(local_msg)
    else:
        print("Running optimisation locally …")
        run_tsp(None, local_msg, False)
else:
    print("First arg: 0 (local) or 1 (RabbitMQ)")

