from math import radians, sin, cos, sqrt, atan2

# Safe Zone Center Coordinates
SAFE_LAT = 11.0168
SAFE_LON = 76.9558

# Radius in meters
SAFE_RADIUS = 200


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two GPS points using Haversine Formula.
    Returns distance in meters.
    """

    R = 6371000  # Earth radius in meters

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        sin(dlat / 2) ** 2
        + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


def check_geofence(current_lat, current_lon):
    """
    Check whether vehicle is inside safe zone.
    """

    distance = calculate_distance(
        SAFE_LAT,
        SAFE_LON,
        current_lat,
        current_lon
    )

    if distance <= SAFE_RADIUS:
        return True, distance

    return False, distance