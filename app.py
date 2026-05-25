# Libraries
import streamlit as st
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Streamlit Page Configuration
st.set_page_config(page_title="Gemini Master Bot", page_icon="🤖", layout="wide")

# Initialize Gemini Client
client = genai.Client()

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.header("⚙️ Model Settings")
    st.write("Fine-tune the chatbot's brain and behavior.")
    
    # AI Persona Selection (Prompt Engineering)
    bot_persona = st.selectbox(
        "Select Bot Persona",
        ["Friendly Buddy", "Coding Mentor", "Strict Assistant"]
    )
    
    # Hyperparameters
    temperature = st.slider("Temperature (Creativity)", min_value=0.0, max_value=2.0, value=1.0, step=0.1)
    max_tokens = st.slider("Max Output Tokens", min_value=100, max_value=4000, value=1500, step=100)
    memory_size = st.slider("Sliding Window Size (Messages)", min_value=4, max_value=20, value=10, step=2)
    
    st.divider()
    
    # Reset Chat History Button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# --- PROMPT ENGINEERING BASED ON PERSONA ---
if bot_persona == "Friendly Buddy":
    system_instruction = "You are a casual, friendly, and energetic AI companion. Use slang like 'bro', 'mate', or 'dude'. Keep the tone relaxed and fun."
elif bot_persona == "Coding Mentor":
    system_instruction = "You are a Senior Software Architect. Your job is to teach coding. Never give the full code solution immediately; guide the user step-by-step with helpful hints."
else:
    system_instruction = "You are a highly professional corporate assistant. Use formal, precise, and polite language. Avoid abbreviations and casual terms."

# Initialize Session State for Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- MAIN INTERFACE ---
st.title("🤖 Gemini Master Web Chatbot")
st.caption("A customizable AI assistant powered by Gemini 3.5-Flash with dynamic prompt engineering and sliding window memory optimization.")
st.divider()

# Display Chat History
for msg in st.session_state.messages:
    avatar = "🧑‍💻" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["parts"][0]["text"])

# User Input Layout
if user_input := st.chat_input("Type your message here..."):
    
    # Display user message
    with st.chat_message("user", avatar="🧑‍💻"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "parts": [{"text": user_input}]})
    
    # SLIDING WINDOW OPTIMIZATION
    while len(st.session_state.messages) > memory_size:
        st.session_state.messages.pop(0)
        
    # Generate AI Response
    try:
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=temperature,
            max_output_tokens=max_tokens
        )
        
        with st.chat_message("model", avatar="🤖"):
            with st.spinner("Thinking..."):
                response = client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=st.session_state.messages,
                    config=config
                )
                st.write(response.text)
                
        st.session_state.messages.append({"role": "model", "parts": [{"text": response.text}]})
        
    except Exception as e:
        st.error(f"An error occurred: {e}")