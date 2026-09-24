import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from config import client, MODEL


QUESTION = "What is a database?"


response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {
            "role": "system",
            "content": (
                "You are a helpful course fee assistant. "
                "Answer the user's question."
            )
        },
        {
            "role": "user",
            "content": QUESTION
        }
    ],
    temperature=0
)


print("=== Plain LLM (No Tool) ===")
print("Question:", QUESTION)
print("Answer:", response.choices[0].message.content)