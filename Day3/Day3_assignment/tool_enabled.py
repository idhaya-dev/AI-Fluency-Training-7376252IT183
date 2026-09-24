import sys
from pathlib import Path
import json

sys.path.append(str(Path(__file__).resolve().parents[2]))

from config import client, MODEL
from tools import get_course_fee


QUESTION = "What is the fee for DS303?"


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_course_fee",
            "description": "Get the fee of a course using its course code.",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_code": {
                        "type": "string",
                        "description": "Course code such as CS101, AI202, or DS303."
                    }
                },
                "required": ["course_code"]
            }
        }
    }
]


messages = [
    {
        "role": "system",
        "content": (
            "You are a course fee assistant. "
            "Use the get_course_fee tool whenever the user asks "
            "for the fee of a specific course."
        )
    },
    {
        "role": "user",
        "content": QUESTION
    }
]


response = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    tools=tools,
    tool_choice="auto",
    temperature=0
)


message = response.choices[0].message


if message.tool_calls:
    tool_call = message.tool_calls[0]

    arguments = json.loads(tool_call.function.arguments)

    print("=== Tool-Enabled LLM ===")
    print("Question:", QUESTION)
    print()
    print("Tool called:", tool_call.function.name)
    print("Arguments:", arguments)

    tool_result = get_course_fee(
        arguments["course_code"]
    )

    print("Tool result:", tool_result)

    messages.append(message)

    messages.append(
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": tool_result
        }
    )

    final_response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0
    )

    print()
    print(
        "Final Answer:",
        final_response.choices[0].message.content
    )

else:
    print("=== Tool-Enabled LLM ===")
    print("Question:", QUESTION)
    print("Final Answer:", message.content)