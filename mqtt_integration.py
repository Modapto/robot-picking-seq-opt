import paho.mqtt.publish as publish
import numpy as np
import json
import traceback
import datetime

def set_message_body(description, production_module, pilot,
                     timestamp, priority, event_type, source_component,
                     smart_service, topic, results):
    message_body = {'description':description, 'module':production_module,
                    'pilot':pilot, 'timestamp':timestamp, 'priority':priority, 'eventType':event_type,
                    'sourceComponent':source_component, 'smartService':smart_service,
                    'topic':topic, 'results':results}
    return message_body

def publish_message(broker, port, auth, description,
                    production_module, pilot, timestamp, priority,
                    event_type, source_component, smart_service, topic, results):
    payload = set_message_body(description, production_module, pilot,
                               timestamp, priority, event_type, source_component,
                               smart_service, topic, results)
    # will = {'topic': topic, 'payload':json.dumps(payload, cls=NpEncoder), 'qos':0, 'retain':False}
    try:
        publish.single(topic=topic, payload=json.dumps(payload, cls=NpEncoder), hostname=broker, port=port, auth=auth)
    except Exception as e:
        print(f"{datetime.datetime.now()}  - Cannot connect to message bus")
        print(traceback.format_exc())


# Extend the JSONEncoder class
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)