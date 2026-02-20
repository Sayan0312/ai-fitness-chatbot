import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

# Safe API key loading
api_key = None

# Try Streamlit secrets (only if exists)
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY not found. Add it to .env (local) or Streamlit secrets (cloud).")
    st.stop()

client = Groq(api_key=api_key)

# Setup Groq client
client = Groq(api_key=api_key)

st.set_page_config(page_title="Fitness AI Coach 💪", page_icon="🏋️")

st.title("🏋️ AI Fitness Coach")
st.write("Ask me about workouts, diet plans, fat loss, muscle gain, etc.")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Ask your fitness question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are a certified fitness coach. Give structured, practical, and safe fitness advice."
                }
            ] + st.session_state.messages
        )
        
        reply = response.choices[0].message.content
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})