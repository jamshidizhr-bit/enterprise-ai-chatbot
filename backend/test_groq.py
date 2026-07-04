import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

print("KEY:", os.getenv("GROQ_API_KEY")[:10] + "...")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

try:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": "Hello"
            }
        ]
    )

    print(response.choices[0].message.content)

except Exception as e:
    print(type(e))
    print(e)