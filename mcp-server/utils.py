import os
import requests
from dotenv import load_dotenv
from prompts import INVENTROY_API_GUIDE  # System prompt template for LLM instructions

load_dotenv()  # Load environment variables from .env file

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = os.getenv("MODEL")  # Model name to use for LLM calls

def format_messages(user_input: str):
    # Compose messages list with system prompt and user input for OpenRouter chat API
    return [
        {"role": "system", "content": INVENTROY_API_GUIDE},
        {"role": "user", "content": user_input}
    ]

async def interpret_query(user_input: str) -> str:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": format_messages(user_input),
    }

    # Send POST request to OpenRouter chat completion API
    response = requests.post(OPENROUTER_URL, headers=headers, json=payload)
    if response.status_code != 200:
        # Raise error if API call fails
        raise Exception(f"OpenRouter API error {response.status_code}: {response.text}")

    result = response.json()
    # Extract the LLM-generated message content
    return result['choices'][0]['message']['content']
