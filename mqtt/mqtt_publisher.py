import json
import random
import time
import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "vehicle/data"

client = mqtt.Client()
client.connect(BROKER, PORT, 60)

print("Connected to MQTT Broker...")

while True:

    vehicle_data = {
        "latitude": round(
            11.0168 + random.uniform(-0.01, 0.01),
            6
        ),
        "longitude": round(
            76.9558 + random.uniform(-0.01, 0.01),
            6
        ),
        "speed": round(
            random.uniform(10, 80),
            2
        ),
        "status": "MOVING"
    }

    payload = json.dumps(vehicle_data)

    client.publish(
        TOPIC,
        payload
    )

    print("Published:", payload)

    time.sleep(5)