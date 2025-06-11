import json, sys, traceback
from datetime import datetime
from time import time
import pika
from pilot_sim_execution import run_simulation
from pilot_opt_execution import run_tsp

def inject_templates(msg: dict) -> None:
    """
    Adds data.containers_template / kit_holders_template / distance_matrix
    so the downstream engine sees exactly what it expects.
    """
    data = msg["data"]
    templates = data.get("templates")
    if templates is None:
        raise ValueError("Missing 'templates' block in payload")

    method = data["method"].lower()

    if method == "simulation":
        data["containers_template"]  = templates["containers_sim"]
        data["kit_holders_template"] = templates["kit_holders_sim"]
        data["distance_matrix"]      = templates["distance_matrix_sim"]
        data["kh_sequences"] = templates["kh_sequences_sim"]

    elif method in {"exact", "linear", "exact-linear"}:
        data["containers_template"]  = templates["containers_opt"]
        data["kit_holders_template"] = templates["kit_holders_opt"]
        data["distance_matrix"]      = templates["distance_matrix_opt"]
        data["kh_sequences"] = templates["kh_sequences_opt"]
    else:
        raise ValueError(f"Unknown method '{method}'")


# ───────────────────── RabbitMQ callback (unchanged messaging) ────────────
def callback(ch, method, properties, body):
    input_file = json.loads(body)
    uuid = input_file["uuid"]
    data = input_file["data"]

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
                          "data": error_message,
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

    inject_templates(input_data)

    if input_data["data"]["method"] == "simulation":
        print("Running simulation...")
        run_simulation(input_data)
    else:
        print("Running optimization...")
        run_tsp(json_file_path=None,
                input_data=input_data,
                generate_new_instance=False)
else:
    print("First argument must be '0' (local) or '1' (RabbitMQ).")