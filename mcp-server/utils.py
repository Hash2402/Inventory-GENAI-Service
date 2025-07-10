import os
import requests 
from dotenv import load_dotenv
from prompts import INVENTROY_API_GUIDE

load_dotenv()

OPENROUTER_API_KEY=os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL=os.getenv("MODEL")

def format_messages(user_input:str):
    return [
        {"role":"system","content":INVENTROY_API_GUIDE},
        {"role":"user","content":user_input}
    ]
    
async def interpret_query(user_input:str)-> str:
    headers={
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": format_messages(user_input),
    }
    
    response = requests.post(OPENROUTER_URL, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"OpenRouter API error {response.status_code}: {response.text}")

    result = response.json()
    return result['choices'][0]['message']['content']