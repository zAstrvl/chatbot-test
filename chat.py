import os
from google import genai
from dotenv import load_dotenv
# Libraries

# Load environment variables from .env file
load_dotenv()

# Initialize the GenAI client with the API key from environment variables
client = genai.Client() 

def chatbot():
    print("🤖 Gemini Chatbot started! Type 'exit' to quit.\n" + "-"*50)

    # Create a new chat session with the specified model
    chat = client.chats.create(model="gemini-3.5-flash")

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