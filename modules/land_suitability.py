import streamlit as st
from streamlit_folium import st_folium
import folium
import requests

def run():
    st.title("🌍 Land Suitability Analyzer")
    st.write("Select your location on the map to analyze soil, rainfall, temperature & elevation, then get best crop suggestions.")

    m = folium.Map(location=[20.5937, 78.9629], zoom_start=4)
    m.add_child(folium.LatLngPopup())  

    map_data = st_folium(m, width=700, height=500)

    if map_data and map_data.get("last_clicked"):
        lat = map_data["last_clicked"]["lat"]
        lon = map_data["last_clicked"]["lng"]
        st.success(f"📍 Selected Location: {lat:.4f}, {lon:.4f}")
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,precipitation_sum&timezone=auto"
        res = requests.get(url).json()

        if "daily" in res:
            temp = sum(res["daily"]["temperature_2m_max"]) / len(res["daily"]["temperature_2m_max"])
            rain = sum(res["daily"]["precipitation_sum"]) / len(res["daily"]["precipitation_sum"])
            st.info(f"🌡 Avg Temp: {temp:.1f} °C | 🌧 Avg Rainfall: {rain:.1f} mm")

            crop_scores = {
                "Wheat": 80 if 10 < temp < 25 else 50,
                "Rice": 85 if temp > 20 and rain > 100 else 40,
                "Maize": 75 if 18 < temp < 30 else 45,
                "Cotton": 70 if temp > 25 else 35,
            }

            st.subheader("🌱 Crop Suitability Ranking")
            sorted_crops = sorted(crop_scores.items(), key=lambda x: x[1], reverse=True)
            for crop, score in sorted_crops:
                st.write(f"**{crop}** — Suitability Score: {score}/100")

            if st.button("Download Report as PDF"):
                st.success("Report generation feature can be added here (using reportlab).")
        else:
            st.error("⚠ Could not fetch weather data. Try another location.")
