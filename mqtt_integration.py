# REPOSITORY NAME (c) by the University of Piraues, Greece.
#
# REPOSITORY NAME is licensed under a
# Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <http://creativecommons.org/licenses/by-nc-nd/3.0/>.

import paho.mqtt.publish as publish
import numpy as np
import json
import traceback
import datetime

def set_message_body(description, production_module, pilot,
                     timestamp, priority, event_type, source_component,
                     smart_service, topic, results):
    """
    Build the message body to be sent over MQTT.
    Returns:
        dict: Dictionary representing the full message body.
    """
    message_body = {'description':description, 'module':production_module,
                    'pilot':pilot, 'timestamp':timestamp, 'priority':priority, 'eventType':event_type,
                    'sourceComponent':source_component, 'smartService':smart_service,
                    'topic':topic, 'results':results}
    return message_body

def publish_message(broker, port, auth, description,
                    production_module, pilot, timestamp, priority,
                    event_type, source_component, smart_service, topic, results):
    """
    Publish a single MQTT message using the given broker configuration.
    """
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
    """
    JSON encoder that converts NumPy types into standard Python types.

    This allows NumPy integers, floats, and arrays to be serialized
    in JSON payloads (e.g. when publishing MQTT messages).
    """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)