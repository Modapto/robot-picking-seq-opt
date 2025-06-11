from pilot_sim_execution import *
from pilot_opt_execution import *

def callback(ch, method, properties, body):
    input_file = json.loads(body)
    uuid = input_file['uuid']
    data = input_file['data']

    try:
        print("%s: Job with uuid: %s received" % (datetime.now().strftime("%d/%m/%Y %H:%M:%S"), uuid))
        input_postman_file_path = "input_postman.json"
        output_postman_file_path = "output_postman.json"
        #Run the TSP algorithm for the JSON input
        if data.get("method") == "simulation":
            output = run_simulation(input_file)
        else:
            output = run_tsp(None, input_file, False)

        print("%s: Publishing results to queue." % (datetime.now().strftime("%d/%m/%Y %H:%M:%S")))

        output = json.dumps(output)
        channel.basic_publish(exchange='opt-result', routing_key='robot-picking-seq', body=output)
        print("%s: Job with uuid: %s completed" % (datetime.now().strftime("%d/%m/%Y %H:%M:%S"), uuid))
    except Exception as e:
        #print(Exception, e)
        print(traceback.format_exc())
        error_message = {"message": "Problem in input data: " + str(e)}
        error_responce = {"uuid": uuid, "data": error_message, "produced_at": int(time() * 1000)}
        error_responce = json.dumps(error_responce)
        channel.basic_publish(exchange='opt-result', routing_key='robot-picking-seq', body=error_responce)
        print("%s: Job with uuid: %s failed" % (datetime.now().strftime("%d/%m/%Y %H:%M:%S"), uuid))


# Main Execution
if online == "1":  # Remote mode with RabbitMQ
    host = sys.argv[2]
    port = sys.argv[3]
    username = sys.argv[4]
    password = sys.argv[5]
    credentials = pika.PlainCredentials(username, password)
    params = pika.ConnectionParameters(host, port, '/', credentials, heartbeat=1860, blocked_connection_timeout=930)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.basic_consume(queue='robot-picking-seq_job', auto_ack=True, on_message_callback=callback)
    channel.start_consuming()

elif online == "0":  # Local mode with JSON file input
    filename = sys.argv[2]
    with open(filename, 'r') as f:
        input_data = json.load(f)

    if input_data["data"]["method"] == "simulation":
        print("Running simulation...")
        run_simulation(input_data)
    else:
        print("Running optimization...")
        run_tsp(json_file_path=filename, input_data=None, generate_new_instance=False)
