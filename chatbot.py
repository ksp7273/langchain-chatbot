import os
import panel as pn
from huggingface_hub import AsyncInferenceClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the Hugging Face Inference Client
client = AsyncInferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.3",
    token=os.environ.get("HF_TOKEN")
)

# System prompt to customize chatbot behavior
SYSTEM_PROMPT = "You are a friendly and helpful assistant. Provide concise, accurate, and engaging responses."

# Asynchronous callback function to handle chat interactions
async def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    # Initialize conversation history
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    # Add conversation history from Panel ChatInterface
    messages.extend([{"role": msg["role"], "content": msg["content"]} for msg in instance.serialize()[1:-1]])
    
    # Add the new user message
    messages.append({"role": "user", "content": contents})
    
    # Get response from Mistral-7B-Instruct-v0.3 (non-streaming)
    response = await client.chat_completion(messages=messages, max_tokens=500)
    message = response.choices[0].message.content
    yield message

# Initialize Panel extension for web-based UI
pn.extension()

# Create the ChatInterface widget with verbose error handling
chat_interface = pn.chat.ChatInterface(
    callback=callback,
    callback_user="Mistral",
    user="You",
    show_clear=False,
    show_undo=False,
    width=800,
    height=500,
    css_classes=["chat-interface"],
    callback_exception="verbose"  # Enable verbose error output
)

# Custom CSS for a polished UI
pn.config.raw_css.append("""
.chat-interface {
    background-color: #f5f5f5;
    border-radius: 10px;
    padding: 15px;
    font-family: Arial, sans-serif;
}
.chat-interface .pn-chat-message {
    border-radius: 8px;
    margin: 5px;
}
.chat-interface .pn-chat-message.user {
    background-color: #007bff;
    color: white;
}
.chat-interface .pn-chat-message.assistant {
    background-color: #e9ecef;
    color: black;
}
""")

# Serve the chat interface
chat_interface.servable()