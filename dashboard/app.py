import streamlit as st
import pandas as pd
import os
from math import radians, sin, cos, sqrt, atan2

# ---------------------------------
# PAGE CONFIG
# ---------------------------------

st.set_page_config(
    page_title="Vehicle Tracking Dashboard",
    page_icon="🚗",
    layout="wide"
)

# ---------------------------------
# GEOFENCE SETTINGS
# ---------------------------------

SAFE_LAT = 11.0168
SAFE_LON = 76.9558
SAFE_RADIUS = 500

# ---------------------------------
# DISTANCE FUNCTION
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
# TITLE
# ---------------------------------

st.title("🚗 IoT Vehicle Tracking & Theft Prevention System")

csv_file = "data/gps_logs.csv"

# ---------------------------------
# CHECK FILE
# ---------------------------------

if os.path.exists(csv_file):

    df = pd.read_csv(csv_file)

    latest = df.iloc[-1]

    lat = latest["Latitude"]
    lon = latest["Longitude"]

    speed = latest["Speed"]

    distance = calculate_distance(
        SAFE_LAT,
        SAFE_LON,
        lat,
        lon
    )

    # -----------------------------
    # ALERT SECTION
    # -----------------------------

    if distance > SAFE_RADIUS:

        st.error(
            f"🚨 THEFT ALERT! Vehicle left safe zone. Distance: {distance:.2f} meters"
        )

    else:

        st.success(
            f"✅ Vehicle inside safe zone. Distance: {distance:.2f} meters"
        )

    # -----------------------------
    # METRICS
    # -----------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Speed",
            f"{speed} km/h"
        )

    with col2:
        st.metric(
            "Latitude",
            round(lat, 6)
        )

    with col3:
        st.metric(
            "Longitude",
            round(lon, 6)
        )

    # -----------------------------
    # GOOGLE MAPS LINK
    # -----------------------------

    st.subheader("📍 Current Location")

    maps_url = f"https://www.google.com/maps?q={lat},{lon}"

    st.markdown(
        f"[Open in Google Maps]({maps_url})"
    )

    # -----------------------------
    # MAP
    # -----------------------------

    st.subheader("🗺 Vehicle Route")

    map_df = pd.DataFrame({
        "lat": df["Latitude"],
        "lon": df["Longitude"]
    })

    st.map(map_df)

    # -----------------------------
    # SPEED GRAPH
    # -----------------------------

    st.subheader("📈 Speed Analysis")

    st.line_chart(df["Speed"])

    # -----------------------------
    # TABLE
    # -----------------------------

    st.subheader("📊 Recent Records")

    st.dataframe(
        df.tail(20),
        use_container_width=True
    )

else:

    st.warning(
        "No GPS Data Found"
    )