import pandas as pd
import requests
from datetime import datetime
import streamlit as st

def load_crop_calendar():
    data = [
        {"Crop": "Wheat", "Region": "North India", "Sowing Period": "Nov - Dec", "Harvest Period": "Mar - Apr"},
        {"Crop": "Rice", "Region": "East India", "Sowing Period": "Jun - Jul", "Harvest Period": "Oct - Nov"},
        {"Crop": "Maize", "Region": "Pan India", "Sowing Period": "Jun - Jul", "Harvest Period": "Oct - Nov"},
        {"Crop": "Millet", "Region": "Central India", "Sowing Period": "Jun - Jul", "Harvest Period": "Oct - Nov"},
        {"Crop": "Sugarcane", "Region": "Pan India", "Sowing Period": "Feb - Apr", "Harvest Period": "Nov - Mar"},
    ]
    return pd.DataFrame(data)

def get_weather_forecast(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=precipitation_sum&timezone=auto"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    rain = data['daily']['precipitation_sum'][0]
    return rain

def show_calendar_and_alert():
    st.subheader("🗓 Crop Calendar & Alerts")

    df = load_crop_calendar()
    st.dataframe(df, use_container_width=True)

    st.markdown("### 🌧 Real-time Rain Alert")

    lat = st.number_input("Enter Latitude", value=28.6139)
    lon = st.number_input("Enter Longitude", value=77.2090)

    if st.button("Check Rain Alert"):
        try:
            rain_mm = get_weather_forecast(lat, lon)
            if rain_mm > 0:
                st.warning(f"🌧 Rain expected today: {rain_mm} mm — Take preventive measures!")
            else:
                st.success("☀️ No rain expected today. Good to proceed with scheduled activities.")
        except Exception as e:
            st.error(f"Failed to fetch weather data: {e}")
