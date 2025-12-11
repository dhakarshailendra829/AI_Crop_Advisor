import streamlit as st
import pandas as pd
import joblib
import numpy as np
from datetime import datetime
from modules.ui_components import load_css
from modules.crop_advisor import recommend_crop
from modules.weather_advisor import get_weather_forecast
from modules.market_advisor import get_market_price
from modules.crop_mapping import get_crop_info  
from PIL import Image
import modules.calandar_advisor as calandar_advisor
import modules.news_fetcher as news_fetcher
from modules import land_suitability       
from modules import ai_chatbot   

st.set_page_config(
    page_title="🌾 AI Crop & Market Advisor",
    layout="wide",
    initial_sidebar_state="collapsed"  
)

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
load_css()

logo_path = "assets/logo.png"
logo = Image.open(logo_path)
st.sidebar.image(logo, use_container_width=True)   
st.sidebar.markdown("### 🌿 AI Crop & Market Advisor")

scaler = joblib.load('models/scaler.pkl')
crop_model = joblib.load('models/crop_model.pkl')
market_df = pd.read_csv('data/mandi_prices.csv')

st.image("assets/logo.png", width=80)
st.markdown("""
<h1 style="text-align:center; font-size:36px; 
            background: linear-gradient(90deg, #007E33, #00C851);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            font-weight:800; margin-bottom:5px;">
🌾 AI Crop & Market Advisor Dashboard
</h1>
<p style="text-align:center; color:#ccc; font-size:16px;">
Empowering Farmers with AI • Weather • Market • Community
</p>
""", unsafe_allow_html=True)

tab_home, tab1, tab2, tab3, tab4, tab_about, tab5, tab6, tab7, tab8 = st.tabs([
    "Home / Dashboard",
    "Crop Recommendation",
    "Weather & Forecast",
    "Market Price Insights",
    "Community Posts",
    "About / Contact / Help",
    "Crop Calendar & Alerts",
    "Agri News & Research",
    "Land Suitability",
    "AI Chatbot"
])

with tab_home:
    st.markdown('<div class="section-title">Home Dashboard</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    try:
        total_crops = market_df['commodity'].nunique()
    except Exception:
        total_crops = 0
    active_states = market_df['state'].nunique()
    try:
        last_update = pd.to_datetime(market_df['Date']).max().strftime("%d %b %Y")
    except Exception:
        last_update = "N/A"

    col1.metric("Total Crops", total_crops)
    col2.metric("Active States", active_states)
    col3.metric("Last Update", last_update)

    st.markdown("### Top 5 Most Traded Crops")
    if not market_df.empty:
        top_crops = market_df['commodity'].value_counts().head(5)
        st.bar_chart(top_crops)
    else:
        st.warning("Market data not available.")

with tab1:
    st.markdown('<div class="section-title">Recommend Best Crop for Your Soil & Weather</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        N = st.number_input("Nitrogen (N)", min_value=0, max_value=200, value=50)
        P = st.number_input("Phosphorus (P)", min_value=0, max_value=200, value=50)
        K = st.number_input("Potassium (K)", min_value=0, max_value=200, value=50)
    with col2:
        temperature = st.number_input("Temperature (°C)", value=25.0)
        humidity = st.number_input("Humidity (%)", value=60.0)
    with col3:
        ph = st.number_input("Soil pH", min_value=0.0, max_value=14.0, value=6.5)
        rainfall = st.number_input("Rainfall (mm)", value=100.0)

    if st.button("Recommend Crop", type="primary"):
        features = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
        try:
            scaled_features = scaler.transform(features)
            crop_label = crop_model.predict(scaled_features)[0]
            crop_info = get_crop_info(crop_label)
            st.success(f"Recommended Crop: **{crop_info['name']}**")
            st.info(f"About {crop_info['name']}: {crop_info['description']}")
        except ValueError as e:
            st.error(f"Error: {e}")

st.markdown('<div class="section-title">Seasonal Crop Guide</div>', unsafe_allow_html=True)

st.markdown("""
<div style="border-radius:12px; overflow:hidden; box-shadow: 3px 3px 10px rgba(0,0,0,0.15); margin-bottom:15px;">
    <div style="background-color:#ff3300; color:white; padding:10px; font-weight:bold; font-size:18px;">
         Summer Crops
    </div>
    <div style="background-color:#fff5f5; padding:15px; color:#333;">
        <ul>
        <li><strong>🍅 Tomato:</strong> Grows in warm weather. Requires regular watering and fertile soil.</li>
        <li><strong>🌶 Chili:</strong> Prefers hot climate. Used for spices and culinary purposes.</li>
        <li><strong>🌽 Maize:</strong> Fast-growing cereal. Needs sunny environment and good soil.</li>
        <li><strong>🫘 Soybean:</strong> Grows well in moderate heat. Improves soil fertility.</li>
        <li><strong>🍆 Brinjal:</strong> Warm-season vegetable. Requires irrigation and sunlight.</li>
        </ul>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="border-radius:12px; overflow:hidden; box-shadow: 3px 3px 10px rgba(0,0,0,0.15); margin-bottom:15px;">
    <div style="background-color:#0047b3; color:white; padding:10px; font-weight:bold; font-size:18px;">
        Winter Crops
    </div>
    <div style="background-color:#e6f0ff; padding:15px; color:#333;">
        <ul>
        <li><strong>🌾 Wheat:</strong> Staple cereal. Thrives in cool climate and moderate rainfall.</li>
        <li><strong>🥕 Carrot:</strong> Root vegetable. Prefers loose, sandy soil.</li>
        <li><strong>🥬 Cabbage:</strong> Leafy vegetable. Needs cool weather and fertile soil.</li>
        <li><strong>🥦 Cauliflower:</strong> Cool-season vegetable. Well-drained soil is necessary.</li>
        <li><strong>🟢 Peas:</strong> Legume crop. Grows in cool conditions and rich soil.</li>
        </ul>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="border-radius:12px; overflow:hidden; box-shadow: 3px 3px 10px rgba(0,0,0,0.15); margin-bottom:15px;">
    <div style="background-color:#008000; color:white; padding:10px; font-weight:bold; font-size:18px;">
        Rainy Season Crops
    </div>
    <div style="background-color:#f0fff0; padding:15px; color:#333;">
        <ul>
        <li><strong>🍚 Rice:</strong> Grows in waterlogged fields. Needs high rainfall.</li>
        <li><strong>🌱 Millet:</strong> Drought-resistant, grows fast in wet or semi-wet regions.</li>
        <li><strong>🥔 Potato:</strong> Prefers cool and wet climate. Tubers develop well.</li>
        <li><strong>🧅 Onion:</strong> Requires moderate rainfall and fertile soil.</li>
        <li><strong>🍆 Brinjal:</strong> Can tolerate rainy conditions with proper drainage.</li>
        </ul>
    </div>
</div>
""", unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="section-title"> Weather & Forecast</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        location = st.text_input("Enter Location", "Delhi")
    with col2:
        date = st.date_input("Date", datetime.today())

    if st.button("Get Weather Forecast"):
        forecast = get_weather_forecast(location, date)
        if forecast:
            st.info(f"{location.title()} - {date.strftime('%d %b %Y')}")
            st.write(forecast)
        else:
            st.warning("No forecast available for this location/date.")

with tab3:
    st.markdown('<div class="section-title">Check Real-time Market Prices</div>', unsafe_allow_html=True)
    market_df.columns = market_df.columns.str.strip().str.title()
    crop_name = st.text_input("Enter Crop Name", "Wheat")
    state_name = st.selectbox("Select State", sorted(market_df['State'].unique()))
    if st.button("Show Market Prices"):
        filtered = market_df[(market_df['Commodity'].str.lower() == crop_name.lower()) &
                             (market_df['State'] == state_name)]
        if not filtered.empty:
            st.dataframe(filtered[['Date', 'State', 'District', 'Market', 'Min_Price', 'Max_Price', 'Modal_Price']])
        else:
            st.warning(f"No price data found for **{crop_name}** in **{state_name}**.")

with tab4:
    st.markdown('<div class="section-title">Community Forum</div>', unsafe_allow_html=True)
    posts_file = "community_posts.csv"
    try:
        posts_df = pd.read_csv(posts_file)
        if 'Replies' not in posts_df.columns:
            posts_df['Replies'] = ""
        else:
            posts_df['Replies'] = posts_df['Replies'].astype(str)
    except FileNotFoundError:
        posts_df = pd.DataFrame(columns=["Name", "Location", "Message", "Date", "Replies"])

    with st.form("community_form"):
        name = st.text_input("Your Name")
        location = st.text_input("Your Location")
        message = st.text_area("Share Your Experience or Ask a Question")
        submitted = st.form_submit_button("Post")
        if submitted and name and message:
            new_post = pd.DataFrame([[name, location, message, datetime.now().strftime("%Y-%m-%d %H:%M"), ""]],
                                    columns=["Name", "Location", "Message", "Date", "Replies"])
            posts_df = pd.concat([posts_df, new_post], ignore_index=True)
            posts_df.to_csv(posts_file, index=False)
            st.success("Post shared successfully!")

    st.subheader("Recent Posts")
    for idx, row in posts_df[::-1].iterrows():
        st.markdown(f"""
        <div class="post-card">
            <strong>{row['Name']}</strong> from <em>{row['Location']}</em><br>
            <span class="message">{row['Message']}</span><br>
            <small>{row['Date']}</small>
        </div>
        """, unsafe_allow_html=True)

        if row['Replies']:
            st.markdown(f"Replies: {row['Replies']}")

        reply_text = st.text_area(f"Reply to {row['Name']}", key=f"reply_{idx}")
        if st.button(f"Submit Reply to {idx}"):
            existing_replies = str(row['Replies'])
            updated_replies = existing_replies + " | " + reply_text if existing_replies else reply_text
            posts_df.at[idx, 'Replies'] = updated_replies
            posts_df.to_csv(posts_file, index=False)
            st.success("Reply added successfully!")

with tab_about:
    st.markdown('<div class="section-title">About the Platform</div>', unsafe_allow_html=True)
    st.write("""
    Welcome to **AI Crop & Market Advisor** — a smart platform designed to help farmers and agri-entrepreneurs make better decisions using **AI, weather data, and market insights**.

    **Key Features:**
    - Crop Recommendation based on soil & weather  
    - Weather Forecast for better planning  
    - Market Price Insights to help get better profits  
    - Community Forum for sharing knowledge

    **Developed by:** Shailendra Dhakad  
    """)

    st.markdown('<div class="section-title">Contact / Support</div>', unsafe_allow_html=True)
    contact_file = "contact_messages.csv"
    try:
        contact_df = pd.read_csv(contact_file)
    except FileNotFoundError:
        contact_df = pd.DataFrame(columns=["Name", "Email", "Message", "Date"])

    with st.form("contact_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Email")
        message = st.text_area("Your Message")
        submitted = st.form_submit_button("Send Message")
        if submitted:
            if name and email and message:
                new_contact = pd.DataFrame([[name, email, message, datetime.now().strftime("%Y-%m-%d %H:%M:%S")]],
                                           columns=["Name", "Email", "Message", "Date"])
                contact_df = pd.concat([contact_df, new_contact], ignore_index=True)
                contact_df.to_csv(contact_file, index=False)
                st.success("Thank you! Your message has been saved.")
            else:
                st.warning("Please fill out all fields before submitting.")

    if not contact_df.empty:
        st.markdown("###Recent Contact Messages")
        st.dataframe(contact_df[::-1])
with tab5:
    calandar_advisor.show_calendar_and_alert()

with tab6:
    news_fetcher.show_news_and_research()
    
with tab7:
    land_suitability.run()  
       
with tab8:
    ai_chatbot.run()