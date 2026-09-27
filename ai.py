import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    raise ValueError("OPENROUTER_API_KEY was not found in .env")


def ask_ai(question):

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Alaska Voice Assistant"
    }

    data = {
            "models": [
    "liquid/lfm-2.5-2.6b:free",
    "inclusionai/ling-3.0-flash-fin:free",
    "qwen/qwen3.8-27b:free"
],
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )

        if response.status_code != 200:
            print("OpenRouter Error:", response.status_code)
            print(response.text)
            return "Sorry, my AI service is temporarily unavailable."

        result = response.json()

        return result["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        print("Connection Error:", e)
        return "Sorry, I am having trouble connecting to the AI service."