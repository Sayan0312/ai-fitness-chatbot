import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Fitness AI Coach 💪",
    page_icon="🏋️",
    layout="centered"
)

# -------------------------------
# CUSTOM CSS (UI UPGRADE)
# -------------------------------
st.markdown("""
<style>

html, body, [class*="css"]  {
    font-family: 'Segoe UI', sans-serif;
}

/* Background Gradient */
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

/* Main Title */
h1 {
    text-align: center;
    font-size: 40px !important;
    font-weight: bold;
}

/* Section Headers */
h2, h3 {
    color: #00f5a0 !important;
}

/* Card effect */
.block-container {
    padding: 2rem 2rem 2rem 2rem;
    border-radius: 20px;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
}

/* Button Styling */
.stButton>button {
    background: linear-gradient(90deg, #00f5a0, #00d9f5);
    color: black;
    font-weight: bold;
    border-radius: 30px;
    height: 3em;
    width: 100%;
    font-size: 18px;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px #00f5a0;
}

/* Chat bubbles */
[data-testid="stChatMessage"] {
    background-color: rgba(255,255,255,0.08);
    border-radius: 15px;
    padding: 10px;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# LOAD API KEY
# -------------------------------
api_key = None
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY not found.")
    st.stop()

client = Groq(api_key=api_key)

# -------------------------------
# TITLE SECTION
# -------------------------------
st.title("🏋️ AI Fitness Coach")
st.markdown("<center>Get a personalized AI-powered fitness & diet plan</center>", unsafe_allow_html=True)
st.markdown("---")

# -------------------------------
# SESSION STATE
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "plan_generated" not in st.session_state:
    st.session_state.plan_generated = False

# -------------------------------
# PROFILE INPUT SECTION (CARD STYLE)
# -------------------------------
st.header("👤 Your Fitness Profile")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", 10, 100, 25)
    height = st.number_input("Height (cm)", 100.0, 250.0, 170.0)
    sleep = st.slider("Sleep (hours/day)", 3, 12, 7)

with col2:
    weight = st.number_input("Weight (kg)", 30.0, 200.0, 70.0)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    exercise = st.selectbox(
        "Exercise Frequency",
        ["None", "1-2 days/week", "3-4 days/week", "5+ days/week"]
    )

goal = st.selectbox(
    "Fitness Goal",
    ["Weight Loss", "Muscle Gain", "Maintain Fitness"]
)

st.markdown("")

# -------------------------------
# GENERATE BUTTON
# -------------------------------
if st.button("💪 Generate My AI Fitness Plan"):

    profile_prompt = f"""
    Create a complete personalized fitness plan.

    User Details:
    Age: {age}
    Gender: {gender}
    Height: {height} cm
    Weight: {weight} kg
    Sleep: {sleep} hours
    Exercise Frequency: {exercise}
    Goal: {goal}

    Include:
    - Weekly workout structure
    - Diet suggestions
    - Sleep optimization
    - Safety precautions
    - Practical tips
    """

    with st.spinner("🔥 Creating your personalized transformation plan..."):

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system",
                 "content": "You are a certified professional fitness coach."},
                {"role": "user",
                 "content": profile_prompt}
            ]
        )

        advice = response.choices[0].message.content

    st.session_state.messages = []
    st.session_state.messages.append(
        {"role": "assistant", "content": advice}
    )

    st.session_state.plan_generated = True

    st.success("✅ Your AI Fitness Plan is Ready!")

st.markdown("---")

# -------------------------------
# CHAT DISPLAY
# -------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------------------
# FOLLOW-UP CHAT
# -------------------------------
if st.session_state.plan_generated:

    st.markdown("### 💬 Ask Follow-Up Questions")

    if user_chat := st.chat_input("Ask about meals, workouts, supplements..."):

        st.session_state.messages.append(
            {"role": "user", "content": user_chat}
        )

        with st.chat_message("user"):
            st.markdown(user_chat)

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are a certified fitness coach. Continue helping based on the existing plan."
                }
            ] + st.session_state.messages
        )

        reply = response.choices[0].message.content

        with st.chat_message("assistant"):
            st.markdown(reply)

        st.session_state.messages.append(
            {"role": "assistant", "content": reply}
        )