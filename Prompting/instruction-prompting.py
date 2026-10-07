from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

INSTRUCTIONS = """
You are a helpful Python programming assistant.

Follow these instructions:
- Answer Pythonrelated q-uestions.
- Explain concepts clearly.
- Use simple examples.
- Keep answers concise.
- If the question is not related to Python, politely say that you
  can only help with Python-related questions.
"""

print("Python Chat Assistant")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    response = client.responses.create(
        model="gpt-4.1-mini",
        instructions=INSTRUCTIONS,
        input=user_input
    )

    print(f"\nAI: {response.output_text}\n")
