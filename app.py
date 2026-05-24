# Libraries
import streamlit as st
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the Streamlit app with a title, icon, and layout
st.set_page_config(page_title="Gemini Master Bot", page_icon="🤖", layout="wide")

# Initialize the GenAI client with the API key from environment variables
client = genai.Client()

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    st.write("Configure your chatbot settings here.")

    bot_role = st.selectbox("Select Bot Role", ["Helpful Assistant", "Technical Expert", "Creative Writer"])

    # Set the system instruction based on the selected bot role to guide the chatbot's responses accordingly
    temperature = st.slider("Response Creativity (Temperature)", min_value=0.0, max_value=2.0, value=1.0, step=0.1)

    # Max tokens for the chatbot's response to ensure it provides comprehensive answers without being too verbose
    max_tokens = st.slider("Max Response Tokens", min_value=50, max_value=1000, value=300, step=50)

    st.divider()
    st.write("💡 *Sliding Window is active: This bot will consider the last few messages in the conversation.*")

# Set the system instruction based on the selected bot role to guide the chatbot's responses accordingly
if bot_role == "Helpful Assistant":
    system_instruction = "You are a helpful and sincere assistant that provides accurate and concise information. Deliver responses in a friendly and engaging manner, ensuring clarity and relevance to the user's queries. Always strive to assist the user to the best of your ability while maintaining a positive and approachable tone."
elif bot_role == "Technical Expert":
    system_instruction = "You are a technical expert with deep knowledge in various fields of technology. Provide detailed and accurate explanations, troubleshooting steps, and insights in a clear and concise manner. Your responses should be informative and helpful, catering to both beginners and advanced users."
elif bot_role == "Creative Writer":
    system_instruction = "You are a creative writer with a flair for storytelling and imaginative responses. Craft engaging and original content that captivates the reader's attention. Your responses should be rich in detail, vivid in description, and evoke emotions while maintaining coherence and relevance to the user's prompts."

# Using a sliding window approach to keep the most recent messages in the conversation history, allowing the chatbot to provide relevant responses without being overwhelmed by too much context
if "messages" not in st.session_state:
    st.session_state.messages = [] # Initialize an empty list to store the conversation history

# UI Title
st.title("🤖 Gemini Master Bot")
st.caption("Powered by Google Gemini 3.5 Flash - A versatile chatbot with adjustable settings and memory management.")

# Writing old messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["parts"][0]["text"])

# New message input
if user_input := st.chat_input("Enter your message..."):
    
    # Write the user's message to the chat interface and add it to the conversation history in session state
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "parts": [{"text": user_input}]})
    
    # Sliding Window Mechanism: Max 6 messages
    while len(st.session_state.messages) > 6:
        st.session_state.messages.pop(0)
        
    # Request to Gemini
    try:
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=temperature,
            max_output_tokens=max_tokens
        )
        
        # When the bot is generating a response, show a spinner to indicate that it's processing the request, and then display the response once it's received. The entire conversation history is sent to the model to maintain context and ensure relevant responses.
        with st.chat_message("model"):
            with st.spinner("Thinking..."):
                response = client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=st.session_state.messages, # Tüm geçmişi paket yapıp yolluyoruz
                    config=config
                )
                st.write(response.text)
                
        # Adding the model's response to the conversation history in session state to maintain context for future interactions
        st.session_state.messages.append({"role": "model", "parts": [{"text": response.text}]})
        
    except Exception as e:
        st.error(f"Bir hata oluştu brom: {e}")