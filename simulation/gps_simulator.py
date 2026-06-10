import random
import time
import pandas as pd
from datetime import datetime

# Starting location (Coimbatore example)
LATITUDE = 11.0168
LONGITUDE = 76.9558

def generate_coordinates():
    """
    Simulate vehicle movement.
    """

    global LATITUDE, LONGITUDE

    LATITUDE += random.uniform(-0.0005, 0.0005)
    LONGITUDE += random.uniform(-0.0005, 0.0005)

    return LATITUDE, LONGITUDE


def save_to_csv(timestamp, lat, lon, speed, status):

    data = {
        "Timestamp": [timestamp],
        "Latitude": [lat],
        "Longitude": [lon],
        "Speed": [speed],
        "Status": [status]
    }

    df = pd.DataFrame(data)

    try:
        df.to_csv(
            "data/gps_logs.csv",
            mode="a",
            header=False,
            index=False
        )

    except FileNotFoundError:
        df.to_csv(
            "data/gps_logs.csv",
            index=False
        )


def main():

    print("Vehicle GPS Simulator Started...\n")

    while True:

        lat, lon = generate_coordinates()

        speed = round(
            random.uniform(10, 80),
            2
        )

        timestamp = datetime.now()

        status = "MOVING"

        save_to_csv(
            timestamp,
            lat,
            lon,
            speed,
            status
        )

        print(f"""
Timestamp : {timestamp}
Latitude  : {lat}
Longitude : {lon}
Speed     : {speed} km/h
Status    : {status}
        """)

        time.sleep(5)


if __name__ == "__main__":
    main()