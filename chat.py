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

    history = [] # Initialize an empty list to store the conversation history

    MAX_HISTORY = 3 # Set a maximum limit for the conversation history to manage context
    # Initial configuration message to set the context for the chatbot's responses
    start_config = (
        "You are a helpful and sincere assistant that provides accurate and concise information. Deliver responses in a friendly and engaging manner, ensuring clarity and relevance to the user's queries. Always strive to assist the user to the best of your ability while maintaining a positive and approachable tone."
    )

    config = types.GenerateContentConfig(
        system_instruction=start_config,
        temperature=0.9, # Adjust the creativity of the responses
        top_p=0.9, # Adjust the diversity of the responses
        top_k=40, # Adjust the number of tokens to consider for generating responses
        max_output_tokens=500, # Set the maximum number of tokens for the chatbot's response
        )

    # Create a new chat session with the specified model
    chat = client.chats.create(
        model="gemini-3.5-flash",
        config=config
        )

    while True:
        user_input = input("You: ") # Input from the user

        # Exit condition to break the loop and end the chatbot session
        if user_input.lower() == "exit" or user_input.lower() == "quit":
            print("🤖 Gemini: Goodbye!")
            break

        # Empty input check
        if not user_input.strip():
            continue

        history.append({"role": "user", "parts": [{"text": user_input}]}) # Add the user's input to the conversation history
        
        # Sliding window mechanism to maintain a manageable conversation history for the chatbot, ensuring it can provide relevant responses without being overwhelmed by too much context
        while len(history) > MAX_HISTORY:
            history.pop(0) # Remove the oldest message from the history if it exceeds the maximum limit

        # Block to handle the chat interaction and catch any exceptions that may occur
        try:
            # Send the user's message to the chat session and get the response
            response = chat.send_message(user_input)

            print(f"🤖 Gemini: {response.text}\n" + "-"*50) # Print the chatbot's response

            history.append({"role": "model", "parts": [{"text": response.text}]}) # Add the chatbot's response to the conversation history
        except Exception as e:
            print(f"❌ An error occurred: {e}\n") # Handle any exceptions that occur during the chat session

if __name__ == "__main__":
    chatbot() # Start the chatbot when the script is run directly