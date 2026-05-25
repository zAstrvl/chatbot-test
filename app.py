# Libraries
import streamlit as st
from google import genai
from google.genai import types
import os
import sqlite3
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Streamlit Page Configuration
st.set_page_config(page_title="chatbot-test", page_icon="🤖", layout="wide")

# Initialize Gemini Client
client = genai.Client()

# DB Setup for Chat History
DB_PATH = "chat_history.db"

# Creates the database and messages table if it doesn't exist
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Load messages from the database
def load_messages_from_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT role, content FROM messages')
    rows = c.fetchall()
    conn.close()

    # Convert DB rows to the format expected by the chatbot interface
    return [{"role": row[0], "parts": [{"text": row[1]}]} for row in rows]

# Save a message to the database
def save_message_to_db(role, content):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO messages (role, content) VALUES (?, ?)', (role, content))
    conn.commit()
    conn.close()

# Clear the database
def clear_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages")
    conn.commit()
    conn.close()

# Trigger database initialization
init_db()

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.header("⚙️ Model Settings")
    
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
        clear_db()
        st.session_state.messages = load_messages_from_db()  # Refresh session state after clearing DB
        st.rerun()

# --- PROMPT ENGINEERING BASED ON PERSONA ---
if bot_persona == "Friendly Buddy":
    system_instruction = "You are a casual, friendly, and energetic AI companion. Use slang like 'bro', 'mate', or 'dude'. Keep the tone relaxed and fun."
elif bot_persona == "Coding Mentor":
    system_instruction = "You are a Senior Software Architect. Your job is to teach coding. Never give the full code solution immediately; guide the user step-by-step with helpful hints."
else:
    system_instruction = "You are a highly professional corporate assistant. Use formal, precise, and polite language. Avoid abbreviations and casual terms."

# --- MEMORY MANAGEMENT ---
# Loads the chat history from the database if it exists (Persistent Memory)
if "messages" not in st.session_state:
    st.session_state.messages = load_messages_from_db()

# --- MAIN INTERFACE ---
st.title("🤖 chatbot-test")
st.caption("A customizable AI assistant powered by Gemini 3.5-Flash with dynamic prompt engineering and sliding window memory optimization.")
st.divider()

# Display Chat History
for msg in st.session_state.messages:
    avatar = "🧑‍💻" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["parts"][0]["text"])

# User Input Layout
if user_input := st.chat_input("Type your message here..."):
    
    # Print user message and save to session state and database
    with st.chat_message("user", avatar="🧑‍💻"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "parts": [{"text": user_input}]})
    save_message_to_db("user", user_input)  # Save user message to DB
    
    # SLIDING WINDOW OPTIMIZATION
    while len(st.session_state.messages) > memory_size:
        st.session_state.messages.pop(0)
        save_message_to_db("model", st.session_state.messages[-1]["parts"][0]["text"])  # Save the popped message to DB

    # Generate AI Response
    try:
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=temperature,
            max_output_tokens=max_tokens
        )
        
        with st.chat_message("model", avatar="🤖"):
            with st.spinner("Thinking..."):
                # Generate response using Gemini 3.5-Flash with streaming
                response = client.models.generate_content_stream(
                    model="gemini-3.5-flash",
                    contents=st.session_state.messages,
                    config=config
                )
                
                full_response = st.write_stream(chunk.text for chunk in response)
                
        st.session_state.messages.append({"role": "model", "parts": [{"text": full_response}]} )
        save_message_to_db("model", full_response)  # Save AI message to DB

    except Exception as e:
        st.error(f"An error occurred: {e}")