import json
import os
import pandas as pd
import paho.mqtt.client as mqtt
from datetime import datetime

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "vehicle/data"

CSV_FILE = "data/gps_logs.csv"


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker")
    client.subscribe(TOPIC)


def on_message(client, userdata, msg):

    payload = json.loads(
        msg.payload.decode()
    )

    print(payload)

    row = {
        "Timestamp": datetime.now(),
        "Latitude": payload["latitude"],
        "Longitude": payload["longitude"],
        "Speed": payload["speed"],
        "Status": payload["status"]
    }

    df = pd.DataFrame([row])

    if not os.path.exists(CSV_FILE):

        df.to_csv(
            CSV_FILE,
            index=False
        )

    else:

        df.to_csv(
            CSV_FILE,
            mode="a",
            header=False,
            index=False
        )


client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect(
    BROKER,
    PORT,
    60
)

client.loop_forever()