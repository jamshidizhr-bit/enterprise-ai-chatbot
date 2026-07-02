from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def stream_ai(message: str):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "تو یک دستیار کاملاً فارسی هستی. فقط فارسی جواب بده."
            },
            {
                "role": "user",
                "content": message
            }
        ],
        temperature=0.3,
        stream=True
    )

    for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            yield content