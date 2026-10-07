from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

SYSTEM_PROMPT = """
You are an LMS support ticket classifier.

Your job is to classify an LMS support ticket into exactly
one of the following categories.

CATEGORIES:

LMS_ADMIN
- The user says a course, activity, lesson, quiz, or module
  is not showing as completed.
- The user completed something but the LMS still shows it as incomplete.
- The user cannot log in.
- The user forgot a password.
- The user has an account or authentication problem.
- The user asks about course enrollment.
- The user cannot enroll in a course.
- The user asks about registration for a course or program.
- The user cannot access a course.
- The course is not visible after enrollment.
- The user says they are enrolled but cannot open the course.

LMS_DEVELOPER
- The user asks about programming error found.
- Any feature/funtionality is not working properly.
- Something went wrong to the LMS.
- LMS is not reachable.
- LMS is not responding as expected.

LMS_MANAGEMENT
- The user asks about a course completion certificate.
- The user cannot download a certificate.
- The user asks when the certificate will be available.

LMS_COURSE_CONTENT
- The user has a question about course content.
- The user says course material is incorrect, missing, or unclear.
- The user asks about lessons, learning material, videos,
  PDFs, or educational content.

LMS_TEACHER
- The user asks about marks, grades, scores, examination results,
  pass/fail status, or result calculation.

LMS_TECHNICAL
- General LMS technical problems.
- Pages are broken.
- Buttons are not working.
- LMS errors or unexpected technical behavior.

OTHER
- The request does not clearly belong to any category above.

IMPORTANT RULES:

1. Return exactly ONE category.
2. Return ONLY the category name.
3. Do not provide an explanation.
4. Choose the category representing the user's PRIMARY issue.
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
        instructions= SYSTEM_PROMPT,
        input=ticket
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

        ticket = input("You: ")

        if ticket.lower() == "exit":
            print("Goodbye!")
            break

        if not ticket.strip():
            print("Please enter a ticket.\n")
            continue

        category = classify_ticket(ticket)

        team = route_ticket(category)

        print(f"\nCategory : {category}")
        print(f"Route To : {team}\n")


if __name__ == "__main__":
    main()

