import pandas as pd
from math import radians, sin, cos, sqrt, atan2
import time

SAFE_LAT = 11.0168
SAFE_LON = 76.9558

SAFE_RADIUS = 500  # meters


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

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


while True:

    try:

        df = pd.read_csv("data/gps_logs.csv")

        latest = df.iloc[-1]

        lat = latest["Latitude"]
        lon = latest["Longitude"]

        distance = calculate_distance(
            SAFE_LAT,
            SAFE_LON,
            lat,
            lon
        )

        print(f"Distance: {distance:.2f} meters")

        if distance > SAFE_RADIUS:

            print("\n🚨 THEFT ALERT 🚨")
            print("Vehicle Outside Safe Zone\n")

        else:

            print("✅ Vehicle Inside Safe Zone")

    except Exception as e:

        print(e)

    time.sleep(5)