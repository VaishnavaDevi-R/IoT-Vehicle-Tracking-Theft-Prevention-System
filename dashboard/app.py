import streamlit as st

st.set_page_config(
    page_title="Vehicle Tracking Dashboard",
    page_icon="🚗"
)

st.title("🚗 IoT Vehicle Tracking & Theft Prevention System")

st.success("MQTT Communication Working Successfully")

st.metric(
    "Vehicle Status",
    "MOVING"
)

st.metric(
    "Speed",
    "65 km/h"
)

st.metric(
    "Location",
    "11.0168, 76.9558"
)