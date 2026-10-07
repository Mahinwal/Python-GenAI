from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

SYSTEM_PROMPT = """
You are an IT support ticket classifier.

Your job is to classify the user's IT support request into exactly
one of the following categories:

NETWORK
HARDWARE
ACCOUNT
SOFTWARE
SECURITY
OTHER

Category definitions:

NETWORK:
Problems related to internet, VPN, Wi-Fi, DNS, connectivity,
network access, or network configuration.

HARDWARE:
Problems related to laptops, desktops, monitors, keyboards,
mouse, printers, or other physical hardware.

ACCOUNT:
Problems related to passwords, login, account access,
authentication, or user accounts.

SOFTWARE:
Problems related to installing, running, updating, or
troubleshooting software applications.

SECURITY:
Problems related to malware, phishing, suspicious activity,
security incidents, or compromised systems.

OTHER:
Requests that do not clearly belong to any of the categories above.

Rules:
- Return exactly one category.
- Return only the category name.
- Do not provide an explanation.
- Choose the category that best represents the primary issue.
"""

def classify_ticket(ticket: str) -> str:
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=ticket,
        instructions= SYSTEM_PROMPT
    )

    return response.output_text.strip()


def route_ticket(category: str) -> str:
    routing = {
        "NETWORK": "Network Support Team",
        "HARDWARE": "Hardware Support Team",
        "ACCOUNT": "Identity & Access Management Team",
        "SOFTWARE": "Software Support Team",
        "SECURITY": "Security Operations Team",
        "OTHER": "General IT Support Team",
    }

    return routing.get(category, "General IT Support Team")


def main():
    print("===================================")
    print("     IT Support Ticket System")
    print("===================================")
    print("Type 'exit' to quit.\n")

    while True:
        ticket = input("Enter support ticket: ")

        if ticket.lower() == 'exit':
            print("Goodby!")
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
