# chatbot-test

A lightweight, high-performance, and fully customizable AI Chatbot interface built with **Python**, **Streamlit**, and the latest official **Google GenAI SDK**. Powered by the cutting-edge `gemini-3.5-flash` model.

This project goes beyond a simple API wrapper by implementing fundamental AI engineering concepts such as **Dynamic Prompt Engineering**, **Sliding Window Memory Optimization**, and **Hyperparameter Tuning**.

## 🚀 Key Features

- **🔄 On-the-Fly Persona Shifting:** Dynamically updates system instructions (Friendly Buddy, Coding Mentor, Strict Assistant) without breaking the ongoing chat session flow.
- **💾 Persistent SQLite Storage:** Chat histories are no longer volatile. Every message is securely committed to a local SQLite database (`chat_history.db`), allowing conversations to persist across browser refreshes, session timeouts, or server restarts.
- **🧠 Adjustable Sliding Window:** Manually controls the context size sent to the Chat Completion API to prevent token bloat, reduce costs, and maintain blazing-fast response speeds.
- **📱 Modern Chat UI:** A clean, responsive, ChatGPT-like web interface powered by Streamlit.
- **🛡️ Secure Token Management:** Zero hardcoded credentials; fully powered by environment variables via `python-dotenv`.
- **🌊 Real-Time Content Streaming:** Implements asynchronous token delivery using `generate_content_stream`. The UI renders responses word-by-word via Streamlit's native streaming API, significantly improving Perceived Latency and User Experience (UX).

## 🛠️ Tech Stack

- **Language:** Python 3.9+
- **LLM Engine:** Google Gemini 3.5-Flash (`google-genai`)
- **Frontend UI:** Streamlit
- **Environment Management:** Python-Dotenv
- **Database:** SQLite3

## 🧠 Architecture & Core Concepts Explained
### 1. The Memory Illusion & Streaming Workflow
LLM endpoints are fundamentally stateless. To deliver a seamless multi-turn conversation, this application aggregates historical interactions into a structured list. 

Instead of waiting for the model to generate the entire response on the backend (which causes high Time-To-First-Token latencies), the app leverages chunk-based generators:

```text
[User Prompt] ➡️ [SQLite Save] ➡️ [Context Compilation] ➡️ [Gemini Stream API]
                                                                  |
[UI Render (st.write_stream)] ⬅️ [Yield Chunk.text] ⬅️ 🌟 Real-time Generation
```
### 2. Sliding Window Optimization
Unmanaged history arrays yield exponential token overhead. By tracking input array sizes dynamically, the buffer automatically drops the earliest multi-turn data points when limits are breached, securing fixed-bound transaction overheads.

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
   or
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure your environment variables:**
   Create a .env file in the root directory and add your Google AI Studio API Key:
   `GEMINI_API_KEY=your_actual_api_key_here`
4. **Run the application:**
   ```bash
   streamlit run app.py
   ```
   