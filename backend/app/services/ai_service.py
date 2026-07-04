import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def ask_ai(message: str):

    try:

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": message
                }
            ],
            temperature=0.7,
        )

        return completion.choices[0].message.content

    except Exception as e:
        print("=" * 50)
        print(type(e))
        print(e)
        print("=" * 50)
        raise