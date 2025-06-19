#!/usr/bin/env python3
import json, sys, traceback, base64, pickle
from datetime import datetime
from time import time
import pika
from pilot_sim_execution import run_simulation
from pilot_opt_execution import run_tsp


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
        data["kh_sequences"]         = templates["kh_sequences_sim"]
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
        data = input_file["data"]

        if data["method"] == "simulation":
            result = run_simulation(input_file)
        else:
            result = run_tsp(None, input_file, False)

        payload = {
            "uuid": uuid,
            "generated_at": int(time() * 1000),
            "data": {
                "base64": base64.b64encode(pickle.dumps(result)).decode()
            }
        }
        ch.basic_publish(exchange='opt-result',
                         routing_key='robot-picking-seq',
                         body=json.dumps(payload))
        print(f"{datetime.now():%d/%m/%Y %H:%M:%S}: Job {uuid} completed")

    except Exception as exc:
        traceback.print_exc()
        err_payload = {
            "uuid": uuid,
            "produced_at": int(time() * 1000),
            "data": {
                "base64": base64.b64encode(
                    pickle.dumps({"message": f"Problem in input data: {exc}"})
                ).decode()
            }
        }
        ch.basic_publish(exchange='opt-result',
                         routing_key='robot-picking-seq',
                         body=json.dumps(err_payload))
        print(f"{datetime.now():%d/%m/%Y %H:%M:%S}: Job {uuid} failed")


# ───────────────────────── entry-point ─────────────────────────
online = sys.argv[1]   # "1" = RabbitMQ,  "0" = local JSON

if online == "1":
    host, port, user, pw = sys.argv[2:6]
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
