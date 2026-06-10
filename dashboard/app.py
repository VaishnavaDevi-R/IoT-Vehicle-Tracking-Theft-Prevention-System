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

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Speed",
            f"{latest['Speed']} km/h"
        )

    with col2:
        st.metric(
            "Latitude",
            round(
                latest["Latitude"],
                6
            )
        )

    with col3:
        st.metric(
            "Longitude",
            round(
                latest["Longitude"],
                6
            )
        )

    st.subheader("🗺 Vehicle Route")

    map_df = pd.DataFrame({
        "lat": df["Latitude"],
        "lon": df["Longitude"]
    })

    st.map(map_df)

    st.subheader("📊 Recent Records")

    st.dataframe(
        df.tail(10),
        use_container_width=True
    )

else:

    st.warning(
        "No GPS Data Found.\nRun mqtt_subscriber.py and mqtt_publisher.py first."
    )