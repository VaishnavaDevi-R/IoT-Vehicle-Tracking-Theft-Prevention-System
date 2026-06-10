from geofence import check_geofence


def detect_theft(lat, lon, vehicle_locked=True):
    """
    Detect theft conditions.
    """

    inside_zone, distance = check_geofence(lat, lon)

    if vehicle_locked and not inside_zone:
        return {
            "status": "THEFT DETECTED",
            "alert": True,
            "distance": round(distance, 2)
        }

    return {
        "status": "SAFE",
        "alert": False,
        "distance": round(distance, 2)
    }


# Testing
if __name__ == "__main__":

    lat = 11.0500
    lon = 76.9900

    result = detect_theft(lat, lon)

    print(result)