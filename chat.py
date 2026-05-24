import os
from google import genai
from dotenv import load_dotenv
from google.genai import types
# Libraries

# Load environment variables from .env file
load_dotenv()

# Initialize the GenAI client with the API key from environment variables
client = genai.Client() 

def chatbot():
    print("🤖 Gemini Chatbot started! Type 'exit' or 'quit' to quit.\n" + "-"*50)

    # Initial configuration message to set the context for the chatbot's responses
    start_config = (
        "You are a helpful and sincere assistant that provides accurate and concise information. Deliver responses in a friendly and engaging manner, ensuring clarity and relevance to the user's queries. Always strive to assist the user to the best of your ability while maintaining a positive and approachable tone."
    )

    config = types.GenerateContentConfig(system_instruction=start_config)

    # Create a new chat session with the specified model
    chat = client.chats.create(model="gemini-3.5-flash", config=config)

    while True:
        user_input = input("You: ") # Input from the user

        # Exit condition to break the loop and end the chatbot session
        if user_input.lower() == "exit" or user_input.lower() == "quit":
            print("🤖 Gemini: Goodbye!")
            break

        # Empty input check
        if not user_input.strip():
            continue
        
        # Block to handle the chat interaction and catch any exceptions that may occur
        try:
            # Send the user's message to the chat session and get the response
            response = chat.send_message(user_input)
            print(f"🤖 Gemini: {response.text}\n" + "-"*50) # Print the chatbot's response
        except Exception as e:
            print(f"❌ An error occurred: {e}\n") # Handle any exceptions that occur during the chat session

if __name__ == "__main__":
    chatbot() # Start the chatbot when the script is run directly