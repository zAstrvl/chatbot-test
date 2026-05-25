# chatbot-test

A lightweight, high-performance, and fully customizable AI Chatbot interface built with **Python**, **Streamlit**, and the latest official **Google GenAI SDK**. Powered by the cutting-edge `gemini-3.5-flash` model.

This project goes beyond a simple API wrapper by implementing fundamental AI engineering concepts such as **Dynamic Prompt Engineering**, **Sliding Window Memory Optimization**, and **Hyperparameter Tuning**.

## 🚀 Key Features

- **Dynamic Personas:** Switch between different system instructions (Friendly Buddy, Coding Mentor, Strict Assistant) on the fly using Prompt Engineering.
- **Sliding Window Memory:** Manually controls the context size sent to the Chat Completion API to prevent token bloat, reduce costs, and maintain blazing-fast response speeds.
- **Hyperparameter Controls:** Real-time adjustments for `temperature` (creativity level) and `max_output_tokens`.
- **Modern Chat UI:** A clean, responsive, ChatGPT-like web interface powered by Streamlit.
- **Secure Configuration:** Zero hardcoded credentials; fully powered by environment variables via `python-dotenv`.

## 🛠️ Tech Stack

- **Language:** Python 3.9+
- **LLM Engine:** Google Gemini 3.5-Flash (`google-genai`)
- **Frontend UI:** Streamlit
- **Environment Management:** Python-Dotenv

## 📦 Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/your-username/gemini-master-chatbot.git](https://github.com/your-username/gemini-master-chatbot.git)
   cd gemini-master-chatbot
   ```
2. **Install Dependencies:**
   ```bash
   pip install streamlit google-genai python-dotenv
   ```
3. **Configure your environment variables:**
   Create a .env file in the root directory and add your Google AI Studio API Key:
   `GEMINI_API_KEY=your_actual_api_key_here`
4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## 🧠 Architecture & Core Concepts Explained
1. Chat Completion & Memory Illusion

LLMs are naturally stateless. To create a continuous conversation flow, this app appends the historical messages into a single array (st.session_state.messages) and sends the entire bundle to the Gemini API with each new prompt.

2. Sliding Window Optimization

Unchecked chat history exponentially increases token usage and API latency. This app introduces a configurable sliding window buffer. When the message count exceeds the set limit, the oldest messages are safely removed (pop(0)) from the context array, keeping the app optimized and cost-efficient.