iimport joblib, json, time
from awsiot.greengrasscoreipc.client import GreengrassCoreIPCClient
from awsiot.greengrasscoreipc.model import SubscribeToIoTCoreRequest, IoTCoreMessage

# Load your trained model (previously downloaded from S3 to Pi)
model = joblib.load('/greengrass/v2/packages/com.example.MLPredictor/1.0.0/model.joblib')

def predict_next_state(current_data):
    X = [[current_data['temperature'], current_data['humidity']]]
    prediction = model.predict(X)[0]
    return {
        "predicted_temperature": prediction[0],
        "predicted_humidity": prediction[1],
    }

def on_message(msg: IoTCoreMessage):
    data = json.loads(msg.payload.decode())
    prediction = predict_next_state(data)
    print(f"Current: {data}, Prediction: {prediction}")

ipc_client = GreengrassCoreIPCClient()

request = SubscribeToIoTCoreRequest(topic_name="raspberrypi/sensors")
operation = ipc_client.subscribe_to_iot_core(request, on_message)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    operation.close()

