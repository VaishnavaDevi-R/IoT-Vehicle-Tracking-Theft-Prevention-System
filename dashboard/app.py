import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Vehicle Tracking Dashboard",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 IoT Vehicle Tracking & Theft Prevention System")

csv_file = "data/gps_logs.csv"

if os.path.exists(csv_file):

    df = pd.read_csv(csv_file)

    latest = df.iloc[-1]

    speed = latest["Speed"]
    latitude = latest["Latitude"]
    longitude = latest["Longitude"]
    distance = latest["Distance"]
    alert = latest["Alert"]

    # Alert Section

    if alert == "THEFT DETECTED":

        st.error(
            f"🚨 THEFT ALERT! Vehicle left safe zone ({distance} meters)"
        )

    else:

        st.success(
            f"✅ Vehicle Inside Safe Zone ({distance} meters)"
        )

    # Metrics

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Speed",
            f"{speed} km/h"
        )

    with col2:
        st.metric(
            "Latitude",
            round(latitude, 6)
        )

    with col3:
        st.metric(
            "Longitude",
            round(longitude, 6)
        )

    with col4:
        st.metric(
            "Distance",
            f"{distance} m"
        )

    # Google Maps Link

    st.subheader("📍 Current Location")

    maps_url = (
        f"https://www.google.com/maps?q={latitude},{longitude}"
    )

    st.markdown(
        f"[🌍 Open in Google Maps]({maps_url})"
    )

    # Route Map

    st.subheader("🗺 Vehicle Route")

    map_df = pd.DataFrame({
        "lat": df["Latitude"],
        "lon": df["Longitude"]
    })

    st.map(map_df)

    # Speed Analytics

    st.subheader("📈 Speed Analytics")

    st.line_chart(df["Speed"])

    # Alert Analytics

    st.subheader("🚨 Alert History")

    st.dataframe(
        df[
            [
                "Timestamp",
                "Alert",
                "Distance"
            ]
        ].tail(20),
        use_container_width=True
    )

    # Recent Records

    st.subheader("📊 Vehicle Logs")

    st.dataframe(
        df.tail(20),
        use_container_width=True
    )

else:

    st.warning(
        "No GPS Data Available"
    )