import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

# Load API key
api_key = None
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY not found.")
    st.stop()

client = Groq(api_key=api_key)

st.set_page_config(page_title="Fitness AI Coach 💪", page_icon="🏋️")

st.title("🏋️ AI Fitness Coach")

# -------------------------------
# PROFILE INPUT SECTION
# -------------------------------

st.header("Enter Your Details")

age = st.number_input("Age", 10, 100, 25)
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
height = st.number_input("Height (cm)", 100.0, 250.0, 170.0)
weight = st.number_input("Weight (kg)", 30.0, 200.0, 70.0)
sleep = st.slider("Sleep (hours/day)", 3, 12, 7)
exercise = st.selectbox(
    "Exercise Frequency",
    ["None", "1-2 days/week", "3-4 days/week", "5+ days/week"]
)
goal = st.selectbox(
    "Fitness Goal",
    ["Weight Loss", "Muscle Gain", "Maintain Fitness"]
)

# Store advice in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "initial_advice" not in st.session_state:
    st.session_state.initial_advice = None

# -------------------------------
# GET FITNESS ADVICE BUTTON
# -------------------------------

if st.button("💪 Get Fitness Advice"):

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
    - Workout plan
    - Diet suggestions
    - Sleep advice
    - Weekly structure
    - Safety tips
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are a certified professional fitness coach."
            },
            {
                "role": "user",
                "content": profile_prompt
            }
        ]
    )

    advice = response.choices[0].message.content

    st.session_state.initial_advice = advice
    st.session_state.messages = [
        {"role": "assistant", "content": advice}
    ]

# -------------------------------
# DISPLAY INITIAL ADVICE
# -------------------------------

if st.session_state.initial_advice:
    st.markdown("## 📝 Your Personalized Plan")
    st.markdown(st.session_state.initial_advice)

# -------------------------------
# CHAT SECTION (After Advice)
# -------------------------------

st.markdown("---")
st.header("💬 Follow-up Questions")

# Show chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_chat := st.chat_input("Ask follow-up or request summary..."):

    st.session_state.messages.append({"role": "user", "content": user_chat})

    with st.chat_message("user"):
        st.markdown(user_chat)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are a certified fitness coach. Continue the conversation based on previous advice."
            }
        ] + st.session_state.messages
    )

    reply = response.choices[0].message.content

    with st.chat_message("assistant"):
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})