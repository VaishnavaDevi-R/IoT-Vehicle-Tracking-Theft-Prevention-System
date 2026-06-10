import streamlit as st
import pandas as pd
import os

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Vehicle Tracking & Theft Prevention System",
    page_icon="🚗",
    layout="wide"
)

# ==================================================
# CUSTOM THEME
# ==================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #0F172A;
}

h1 {
    text-align: center;
    color: white !important;
    font-weight: 800 !important;
}

h2,h3 {
    color: #E2E8F0 !important;
}

[data-testid="metric-container"] {
    background: #1E293B;
    border-radius: 18px;
    padding: 15px;
    border: 1px solid rgba(255,255,255,0.08);
}

[data-testid="stDataFrame"] {
    border-radius: 15px;
    overflow: hidden;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# HEADER
# ==================================================

st.title("🚗 Vehicle Tracking & Theft Prevention System")

st.caption(
    "Real-Time GPS Tracking • Geofencing • Theft Detection"
)

# ==================================================
# CSV FILE
# ==================================================

csv_file = "data/gps_logs.csv"

if not os.path.exists(csv_file):

    st.warning(
        "No GPS data found. Run the MQTT publisher and subscriber first."
    )

    st.stop()

# ==================================================
# LOAD DATA
# ==================================================

df = pd.read_csv(csv_file)

latest = df.iloc[-1]

speed = latest["Speed"]
latitude = latest["Latitude"]
longitude = latest["Longitude"]
distance = latest["Distance"]
alert = latest["Alert"]
status = latest["Status"]
timestamp = latest["Timestamp"]

# ==================================================
# VEHICLE INFORMATION
# ==================================================

st.markdown("## 🚗 Vehicle Information")

info1, info2, info3 = st.columns(3)

with info1:
    st.info("Vehicle ID : VH-001")

with info2:
    st.info(f"Current Status : {status}")

with info3:
    st.info(f"Last Update : {timestamp}")

# ==================================================
# MAIN METRICS
# ==================================================

metric1, metric2, metric3, metric4 = st.columns(4)

with metric1:
    st.metric(
        "⚡ Speed",
        f"{speed} km/h"
    )

with metric2:
    st.metric(
        "📍 Distance",
        f"{distance:.2f} m"
    )

with metric3:
    st.metric(
        "🚨 Alert",
        alert
    )

with metric4:
    st.metric(
        "🛰️ GPS Status",
        "ACTIVE"
    )

# ==================================================
# MAP + SECURITY OVERVIEW
# ==================================================

left, right = st.columns([2,1])

with left:

    st.markdown("## 🗺️ Live Vehicle Location")

    map_df = pd.DataFrame({
        "lat": [latitude],
        "lon": [longitude]
    })

    st.map(
        map_df,
        use_container_width=True
    )

    st.link_button(
        "📍 Open in Google Maps",
        f"https://www.google.com/maps?q={latitude},{longitude}"
    )

with right:

    st.markdown("## 🚨 Security Overview")

    if alert == "THEFT DETECTED":

        st.error("THEFT DETECTED")

        st.metric(
            "Threat Level",
            "HIGH"
        )

        st.metric(
            "Zone Status",
            "OUTSIDE SAFE ZONE"
        )

    else:

        st.success("SAFE")

        st.metric(
            "Threat Level",
            "LOW"
        )

        st.metric(
            "Zone Status",
            "INSIDE SAFE ZONE"
        )

    st.metric(
        "Distance From Safe Zone",
        f"{distance:.2f} m"
    )

# ==================================================
# TRACKING ANALYTICS
# ==================================================

st.markdown("---")

st.markdown("## 📊 Tracking Analytics")

avg_speed = round(
    df["Speed"].mean(),
    2
)

max_speed = round(
    df["Speed"].max(),
    2
)

min_speed = round(
    df["Speed"].min(),
    2
)

total_alerts = len(
    df[
        df["Alert"] == "THEFT DETECTED"
    ]
)

a, b, c, d = st.columns(4)

with a:
    st.metric(
        "Average Speed",
        avg_speed
    )

with b:
    st.metric(
        "Maximum Speed",
        max_speed
    )

with c:
    st.metric(
        "Minimum Speed",
        min_speed
    )

with d:
    st.metric(
        "Total Alerts",
        total_alerts
    )

st.line_chart(
    df["Speed"]
)

# ==================================================
# RECENT TRACKING EVENTS
# ==================================================

st.markdown("---")

st.markdown("## 📜 Recent Tracking Events")

recent_events = []

for _, row in df.tail(10).iterrows():

    if row["Alert"] == "THEFT DETECTED":

        recent_events.append(
            f"🚨 {row['Timestamp']} - Theft Alert Triggered"
        )

    else:

        recent_events.append(
            f"✅ {row['Timestamp']} - Vehicle Moving Safely"
        )

for event in reversed(recent_events):

    st.write(event)

# ==================================================
# ROUTE HISTORY
# ==================================================

st.markdown("---")

st.markdown("## 🛣️ Route History")

route_df = pd.DataFrame({
    "lat": df["Latitude"],
    "lon": df["Longitude"]
})

st.map(
    route_df,
    use_container_width=True
)

# ==================================================
# TRACKING LOGS
# ==================================================

st.markdown("---")

st.markdown("## 📋 Tracking Logs")

st.dataframe(
    df.tail(25),
    use_container_width=True
)
