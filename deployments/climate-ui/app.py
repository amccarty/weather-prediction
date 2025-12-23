"""
Climate Prediction Dashboard

Streamlit app to visualize climate predictions from the ClimateAPI.
"""

import streamlit as st
import requests
import pandas as pd

# Configure page
st.set_page_config(
    page_title="Climate Prediction Dashboard",
    page_icon="🌍",
    layout="wide"
)

# API configuration
API_URL = "http://climate-api:8000"  # Internal service name in Outerbounds

# Title and description
st.title("🌍 Climate Change Impact Predictor")
st.markdown("View climate predictions and alerts for major US cities")

# Sidebar for region selection
st.sidebar.header("Settings")

# Get available regions from API
try:
    status_response = requests.get(f"{API_URL}/status", timeout=5)
    if status_response.ok:
        status_data = status_response.json()
        regions = status_data.get("available_regions", [
            "Austin, TX", "Miami, FL", "Phoenix, AZ", "Seattle, WA"
        ])
        api_status = "✅ Connected"
    else:
        regions = ["Austin, TX", "Miami, FL", "Phoenix, AZ", "Seattle, WA"]
        api_status = "⚠️ Using defaults"
except Exception as e:
    regions = ["Austin, TX", "Miami, FL", "Phoenix, AZ", "Seattle, WA"]
    api_status = f"❌ Error: {str(e)}"

st.sidebar.metric("API Status", api_status)

selected_region = st.sidebar.selectbox("Select Region", regions)

# Refresh button
if st.sidebar.button("🔄 Refresh Data"):
    st.rerun()

# Main content area
col1, col2 = st.columns(2)

# Fetch predictions for selected region
try:
    pred_response = requests.get(
        f"{API_URL}/predictions/{selected_region}",
        timeout=5
    )

    if pred_response.ok:
        pred_data = pred_response.json()

        # Temperature predictions
        with col1:
            st.subheader("🌡️ Temperature Change")
            temp_change = pred_data.get("predicted_temp_change", {})

            temp_df = pd.DataFrame({
                "Horizon": ["1 Year", "5 Years", "10 Years"],
                "Temperature Change (°C)": [
                    temp_change.get("1_year", 0),
                    temp_change.get("5_year", 0),
                    temp_change.get("10_year", 0),
                ]
            })

            st.line_chart(temp_df.set_index("Horizon"))

            # Show values in table
            st.dataframe(temp_df, use_container_width=True)

        # Precipitation predictions
        with col2:
            st.subheader("💧 Precipitation Change")
            precip_change = pred_data.get("predicted_precip_change", {})

            precip_df = pd.DataFrame({
                "Horizon": ["1 Year", "5 Years", "10 Years"],
                "Precipitation Change (mm)": [
                    precip_change.get("1_year", 0),
                    precip_change.get("5_year", 0),
                    precip_change.get("10_year", 0),
                ]
            })

            st.line_chart(precip_df.set_index("Horizon"))

            # Show values in table
            st.dataframe(precip_df, use_container_width=True)

        # Extreme events
        st.subheader("⚠️ Extreme Event Probabilities")
        extreme_events = pred_data.get("extreme_event_probabilities", {})

        event_df = pd.DataFrame({
            "Event Type": ["Heatwave", "Drought", "Flood", "Cold Snap"],
            "Probability": [
                extreme_events.get("heatwave", 0),
                extreme_events.get("drought", 0),
                extreme_events.get("flood", 0),
                extreme_events.get("cold_snap", 0),
            ]
        })

        st.bar_chart(event_df.set_index("Event Type"))

        # Last updated
        last_updated = pred_data.get("last_updated", "Unknown")
        st.info(f"📅 Last updated: {last_updated}")

    else:
        st.error(f"Failed to fetch predictions: {pred_response.status_code}")

except Exception as e:
    st.error(f"Error connecting to API: {str(e)}")
    st.info("Make sure the climate-api service is running")

# Alerts section
st.divider()
st.subheader("🚨 Active Climate Alerts")

try:
    alerts_response = requests.get(f"{API_URL}/alerts", timeout=5)

    if alerts_response.ok:
        alerts_data = alerts_response.json()
        alerts = alerts_data.get("alerts", [])

        if alerts:
            for alert in alerts:
                severity_color = "🔴" if alert["severity"] == "high" else "🟡"
                st.warning(
                    f"{severity_color} **{alert['type'].upper()}** in {alert['region']} "
                    f"- {alert['probability']:.1%} probability"
                )
        else:
            st.success("✅ No active climate alerts")
    else:
        st.warning("Could not fetch alerts")

except Exception as e:
    st.warning(f"Could not fetch alerts: {str(e)}")

# Footer
st.divider()
st.caption("Climate Change Impact Predictor - Powered by Metaflow and Outerbounds")
