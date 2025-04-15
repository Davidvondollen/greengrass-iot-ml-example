import json, time, random
from awsiot.greengrasscoreipc.client import GreengrassCoreIPCClient
from awsiot.greengrasscoreipc.model import PublishToIoTCoreRequest, QOS

TOPIC = "raspberrypi/sensors"

def read_sensor():
    return {
        "timestamp": int(time.time()),
        "temperature": random.uniform(20, 30),
        "humidity": random.uniform(40, 60)
    }

ipc_client = GreengrassCoreIPCClient()

while True:
    data = read_sensor()
    payload = json.dumps(data).encode()
    ipc_client.publish_to_iot_core(PublishToIoTCoreRequest(
        topic_name=TOPIC,
        qos=QOS.AT_LEAST_ONCE,
        payload=payload
    ))
    print(f"Published: {data}")
    time.sleep(10)

