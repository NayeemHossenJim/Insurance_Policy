
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/predict"

# Custom CSS for modern look
st.markdown("""
    <style>
    .main {background-color: #f7f9fa;}
    .stButton>button {background-color: #4F8BF9; color: white; font-weight: bold;}
    .stTextInput>div>input {border-radius: 8px;}
    .stNumberInput>div>input {border-radius: 8px;}
    .stSelectbox>div>div {border-radius: 8px;}
    .result-card {background: #eaf6ff; border-radius: 12px; padding: 20px; margin-top: 20px;}
    </style>
""", unsafe_allow_html=True)

# Sidebar branding
st.sidebar.image("https://img.icons8.com/color/96/insurance.png", width=80)
st.sidebar.title("🛡️ Insurance Predictor")
st.sidebar.markdown("""
**Welcome!**

Predict your insurance premium category with confidence. Fill in your details and get instant results!
""")

st.title("✨ Insurance Premium Category Predictor")
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("#### Please enter your details:")

# Input fields in columns for better layout
col1, col2 = st.columns(2)
with col1:
    age = st.number_input("🎂 Age", min_value=1, max_value=119, value=30)
    weight = st.number_input("🏋️ Weight (kg)", min_value=1.0, value=65.0)
    city = st.text_input("🏙️ City", value="Mumbai")
with col2:
    height = st.number_input("📏 Height (m)", min_value=0.5, max_value=2.5, value=1.7)
    income_lpa = st.number_input("💰 Annual Income (LPA)", min_value=0.1, value=10.0)
    smoker = st.selectbox("🚬 Are you a smoker?", options=[True, False])

occupation = st.selectbox(
    "💼 Occupation",
    ['retired', 'freelancer', 'student', 'government_job', 'business_owner', 'unemployed', 'private_job']
)

st.markdown("<br>", unsafe_allow_html=True)
predict_btn = st.button("🔮 Predict Premium Category", use_container_width=True)

if predict_btn:
    input_data = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }

    with st.spinner("Contacting prediction server..."):
        try:
            response = requests.post(API_URL, json=input_data)
            result = response.json()

            if response.status_code == 200 and "response" in result:
                prediction = result["response"]
                st.markdown(
                    f"<div class='result-card'>"
                    f"<h3>✅ Predicted Category: <span style='color:#4F8BF9'>{prediction['predicted_category']}</span></h3>"
                    f"<b>🔍 Confidence:</b> <progress value='{prediction['confidence']}' max='1' style='width:150px'></progress> {prediction['confidence']:.2f}"
                    f"<br><b>📊 Class Probabilities:</b>"
                    f"</div>", unsafe_allow_html=True
                )
                st.json(prediction["class_probabilities"])
            else:
                st.error(f"API Error: {response.status_code}")
                st.write(result)

        except requests.exceptions.ConnectionError:
            st.error("❌ Could not connect to the FastAPI server. Make sure it's running.")