import requests

# Your ThingSpeak Write API Key
API_KEY = "A1J8G4WWSMGJGNAV"

def send_to_thingspeak(
    latitude,
    longitude,
    speed,
    status,
    distance,
    alert
):

    url = "https://api.thingspeak.com/update"

    payload = {
        "api_key": API_KEY,
        "field1": latitude,
        "field2": longitude,
        "field3": speed,
        "field4": status,
        "field5": distance,
        "field6": alert
    }

    response = requests.get(
        url,
        params=payload,
        timeout=10
    )

    print("ThingSpeak Response:", response.text)


# Test
if __name__ == "__main__":

    send_to_thingspeak(
        11.0168,
        76.9558,
        65,
        "MOVING",
        120,
        "SAFE"
    )