import json
import os
import sys
import pandas as pd
import paho.mqtt.client as mqtt
from datetime import datetime
from math import radians, sin, cos, sqrt, atan2

# Add project root path
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from thingspeak.thingspeak_sender import send_to_thingspeak

# ---------------------------------
# MQTT CONFIG
# ---------------------------------

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "vehicle/data"

CSV_FILE = "data/gps_logs.csv"

# ---------------------------------
# GEOFENCE CONFIG
# ---------------------------------

SAFE_LAT = 11.0168
SAFE_LON = 76.9558

SAFE_RADIUS = 500  # meters

# ---------------------------------
# DISTANCE CALCULATION
# ---------------------------------

def calculate_distance(lat1, lon1, lat2, lon2):

    R = 6371000

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1))
        * cos(radians(lat2))
        * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )

    return R * c


# ---------------------------------
# MQTT EVENTS
# ---------------------------------

def on_connect(client, userdata, flags, rc):

    print("Connected to MQTT Broker")

    client.subscribe(TOPIC)


def on_message(client, userdata, msg):

    try:

        payload = json.loads(
            msg.payload.decode()
        )

        latitude = payload["latitude"]
        longitude = payload["longitude"]
        speed = payload["speed"]
        status = payload["status"]

        # -----------------------------
        # Geofence Check
        # -----------------------------

        distance = calculate_distance(
            SAFE_LAT,
            SAFE_LON,
            latitude,
            longitude
        )

        if distance > SAFE_RADIUS:

            alert = "THEFT DETECTED"

            print("\n🚨 THEFT ALERT 🚨")
            print(
                f"Vehicle left safe zone ({distance:.2f} meters)"
            )

        else:

            alert = "SAFE"

            print(
                f"\n✅ Vehicle Inside Safe Zone ({distance:.2f} meters)"
            )

        # -----------------------------
        # CSV LOGGING
        # -----------------------------

        row = {
            "Timestamp": datetime.now(),
            "Latitude": latitude,
            "Longitude": longitude,
            "Speed": speed,
            "Status": status,
            "Distance": round(distance, 2),
            "Alert": alert
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

        print("CSV Updated Successfully")

        # -----------------------------
        # THINGSPEAK UPDATE
        # -----------------------------

        send_to_thingspeak(
            latitude,
            longitude,
            speed,
            status,
            round(distance, 2),
            alert
        )

        print("ThingSpeak Updated Successfully")

    except Exception as e:

        print("Error:", e)


# ---------------------------------
# MQTT CLIENT
# ---------------------------------

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect(
    BROKER,
    PORT,
    60
)

print("\nWaiting for Vehicle Data...\n")

client.loop_forever()