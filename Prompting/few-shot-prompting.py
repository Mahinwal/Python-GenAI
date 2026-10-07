from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()


SYSTEM_PROMPT = """
You are an LMS support ticket classifier.

Your job is to classify an LMS support ticket into exactly
one of the following categories:

LMS_ADMIN
LMS_DEVELOPER
LMS_MANAGEMENT
LMS_COURSE_CONTENT
LMS_TEACHER
OTHER


Here are examples showing how tickets should be classified.


Example 1:

Ticket:
"I completed Module 3 but it still shows as incomplete."

Category:
LMS_ADMIN


Example 2:

Ticket:
"I completed the course but cannot download my certificate."

Category:
LMS_ADMIN


Example 3:

Ticket:
"The explanation in Module 4 is incorrect."

Category:
LMS_COURSE_CONTENT


Example 4:

Ticket:
"My exam marks are not showing."

Category:
LMS_TEACHER


Example 5:

Ticket:
"I forgot my LMS password."

Category:
LMS_ADMIN


Example 6:

Ticket:
"I am unable to enroll in the course."

Category:
LMS_ADMIN


Example 8:

Ticket:
"I enrolled in the course but it isn't visible in my dashboard."

Category:
LMS_ADMIN


Example 9:

Ticket:
"The Submit button is not working in the LMS."

Category:
LMS_DEVELOPER


Rules:

- Return exactly ONE category.
- Return ONLY the category name.
- Do not provide an explanation.
- Choose the category representing the user's PRIMARY issue.
"""


ROUTING = {
    "LMS_ADMIN": "LMS Admin",
    "LMS_DEVELOPER": "LMS Developer",
    "LMS_MANAGEMENT": "LMS Manager",
    "LMS_COURSE_CONTENT": "LMS Content Creator",
    "LMS_TEACHER": "LMS Teacher",
    "LMS_TECHNICAL": "LMS Developer",
    "OTHER": "LMS Manager",
}


def classify_ticket(ticket: str) -> str:

    response = client.responses.create(
        model="gpt-4o-mini",
        instructions=SYSTEM_PROMPT,
        input=ticket,
    )

    return response.output_text.strip()


def route_ticket(category: str) -> str:

    return ROUTING.get(
        category,
        "LMS Manager"
    )


def main():

    print("=" * 50)
    print("          LMS Ticket Classifier")
    print("=" * 50)

    print("Type 'exit' to quit.\n")

    while True:

        ticket = input("User: ")

        if ticket.lower() == "exit":
            break

        if not ticket.strip():
            continue

        category = classify_ticket(ticket)

        team = route_ticket(category)

        print(f"\nCategory : {category}")
        print(f"Route To : {team}\n")


if __name__ == "__main__":
    main()