import json, sys, traceback
from datetime import datetime
from time import time
import pika
from co_pilot_sim_execution import run_simulation
from co_pilot_opt_execution import run_tsp
import base64
import pickle
import copy


# def inject_templates(msg: dict) -> None:
#     """
#     • If msg['data'] is wrapped as  {'base64': "<b64-string>"}
#       → decode / unpickle it in-place.
#     • Then copy the correct templates into
#         data.containers_template, kit_holders_template,
#         distance_matrix, kh_sequences
#       based on data.method
#     """
#     # ---------- unwrap base64-encoded block, if present ----------
#     if isinstance(msg.get("data"), dict) and "base64" in msg["data"]:
#         try:
#             raw_bytes = base64.b64decode(msg["data"]["base64"])
#             msg["data"] = pickle.loads(raw_bytes)
#         except Exception as exc:
#             raise ValueError(f"Failed to decode base64 data: {exc}")
#
#     data = msg["data"]            # <- now a **plain** dict
#
#     # data = msg["data"]
#     templates = data.get("templates")
#     if templates is None:
#         raise ValueError("Missing 'templates' block in payload")
#
#     method = data["method"].lower()
#
#     if method == "simulation":
#         data["containers_template"]  = templates["containers_sim"]
#         data["kit_holders_template"] = templates["kit_holders_sim"]
#         data["distance_matrix"]      = templates["distance_matrix_sim"]
#         data["kh_sequences"] = templates["kh_sequences_sim"]
#
#     elif method in {"exact", "linear", "exact-linear"}:
#         data["containers_template"]  = templates["containers_opt"]
#         data["kit_holders_template"] = templates["kit_holders_opt"]
#         data["distance_matrix"]      = templates["distance_matrix_opt"]
#         data["kh_sequences"] = templates["kh_sequences_opt"]
#     else:
#         raise ValueError(f"Unknown method '{method}'")


# ───────────────────── RabbitMQ callback (unchanged messaging) ────────────
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



def callback(ch, method, properties, body):
    input_file = json.loads(body)
    uuid = input_file['uuid']
    print(input_file['data'])

    file_content = input_file['data']
    try:
        data = pickle.loads(base64.b64decode(file_content))
    except:
        data = copy.deepcopy(file_content)

    # input_file = json.loads(body)
    # uuid = input_file["uuid"]
    # data = input_file["data"]

    try:
        print("%s: Job with uuid: %s received" %
              (datetime.now().strftime("%d/%m/%Y %H:%M:%S"), uuid))

        # NEW: splice the correct templates into the packet
        inject_templates(input_file)

        # ------------------------------------------------------------------
        # Run the TSP algorithm for the JSON input
        if data.get("method") == "simulation":
            output = run_simulation(input_file)
        else:
            output = run_tsp(None, input_file, False)
        # ------------------------------------------------------------------
        output = {'uuid': uuid,
                  'produced_at': int(time() * 1000),
                  'data': {'base64': base64.b64encode(pickle.dumps(output)).decode()}
                  }

        print("%s: Publishing results to queue." %
              (datetime.now().strftime("%d/%m/%Y %H:%M:%S")))

        output = json.dumps(output)
        channel.basic_publish(exchange='opt-result',
                              routing_key='robot-picking-seq',
                              body=output)
        print("%s: Job with uuid: %s completed" %
              (datetime.now().strftime("%d/%m/%Y %H:%M:%S"), uuid))

    except Exception as e:
        print(traceback.format_exc())
        error_message = {"message": "Problem in input data: " + str(e)}
        error_responce = {"uuid": uuid,
                          "data": {'base64': base64.b64encode(pickle.dumps(output)).decode()},
                          "produced_at": int(time() * 1000)}
        error_responce = json.dumps(error_responce)
        channel.basic_publish(exchange='opt-result',
                              routing_key='robot-picking-seq',
                              body=error_responce)
        print("%s: Job with uuid: %s failed" %
              (datetime.now().strftime("%d/%m/%Y %H:%M:%S"), uuid))

online = sys.argv[1]

if online == "1":
    host, port, username, password = sys.argv[2:6]
    credentials = pika.PlainCredentials(username, password)
    params = pika.ConnectionParameters(host, int(port), '/', credentials,
                                       heartbeat=1860,
                                       blocked_connection_timeout=930)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.basic_consume(queue='robot-picking-seq_job',
                          auto_ack=True,
                          on_message_callback=callback)
    channel.start_consuming()

elif online == "0":
    filename = sys.argv[2]
    with open(filename, 'r') as f:
        input_data = json.load(f)

    uuid = input_data['uuid']
    print(input_data['data'])

    # file_content = input_data['data']
    # try:
    #     data = pickle.loads(base64.b64decode(file_content))
    # except:
    #     data = copy.deepcopy(file_content)

    inject_templates(input_data)

    if input_data.get("method") == "simulation":
        print("Running simulation...")
        run_simulation(input_data)
    else:
        print("Running optimization...")
        run_tsp(json_file_path=None,
                input_data=input_data,
                generate_new_instance=False)
else:
    print("First argument must be '0' (local) or '1' (RabbitMQ).")