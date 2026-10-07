import json
import subprocess

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI()

MODEL = "gpt-4o-mini"


# ============================================================
# Git utility functions
# ============================================================

def run_command(cmd: list[str]) -> str:
    """Run a shell command and return its output."""

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        return f"ERROR: {result.stderr.strip()}"

    return result.stdout.strip()


def git_status() -> str:
    """Show changed, staged and untracked files."""

    return run_command(
        ["git", "status", "--short"]
    )


def git_diff() -> str:
    """Show the actual code changes."""

    return run_command(
        ["git", "diff"]
    )


def git_add() -> str:
    """Stage all current changes."""

    return run_command(
        ["git", "add", "."]
    )


def git_commit(message: str) -> str:
    """Commit staged changes."""

    if not message:
        message = "Update via git agent"

    return run_command(
        ["git", "commit", "-m", message]
    )


def git_push() -> str:
    """Push the current branch to the configured remote."""

    return run_command(
        ["git", "push"]
    )


# ============================================================
# Map tool name -> Python function
# ============================================================

AVAILABLE_FUNCTIONS = {
    "git_status": git_status,
    "git_diff": git_diff,
    "git_add": git_add,
    "git_commit": git_commit,
    "git_push": git_push,
}


# ============================================================
# OpenAI tools
# ============================================================

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "git_status",
            "description": (
                "Show changed, staged and untracked files "
                "in the current Git repository."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "git_diff",
            "description": (
                "Show the actual code changes in the "
                "current Git repository."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "git_add",
            "description": (
                "Stage all current changes using git add."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "git_commit",
            "description": (
                "Commit the staged changes using the supplied "
                "commit message."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": (
                            "A concise commit message describing "
                            "the actual code changes."
                        ),
                    }
                },
                "required": ["message"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "git_push",
            "description": (
                "Push the committed changes to the configured "
                "remote Git repository."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
]


# ============================================================
# System prompt
# ============================================================

SYSTEM_PROMPT = """
You are a careful Git coding assistant.

Your job is to manage Git operations when the user asks
you to commit or push their code.

Follow this workflow:

1. Call git_status first.
2. If there are no changes, stop and tell the user.
3. Call git_diff to inspect the actual code changes.
4. Understand what was changed.
5. Generate a concise and meaningful commit message
   based on the actual changes.
6. Call git_add.
7. Call git_commit using the generated commit message.
8. Call git_push.

Important rules:

- Always check git_status first.
- Always inspect git_diff before creating a commit message.
- Do not invent a commit message without looking at the changes.
- The commit message must describe the actual changes.
- Do not modify source code.
- Do not execute arbitrary shell commands.
- If a Git command returns an error, stop the workflow.
- Briefly explain what you are doing.
"""


# ============================================================
# Agent
# ============================================================

def run_agent(user_input: str, history: list) -> list:
    """Run the OpenAI agent."""

    history.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    while True:

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                *history,
            ],
            tools=TOOLS,
            tool_choice="auto",
        )

        message = response.choices[0].message

        # ----------------------------------------------------
        # No tool call means the model has finished.
        # ----------------------------------------------------

        if not message.tool_calls:

            history.append(
                {
                    "role": "assistant",
                    "content": message.content or "",
                }
            )

            print(
                f"\nAgent: {message.content}\n"
            )

            return history

        # ----------------------------------------------------
        # Add assistant's tool call to conversation history.
        # ----------------------------------------------------

        history.append(
            {
                "role": "assistant",
                "content": message.content,
                "tool_calls": [
                    tool_call.model_dump()
                    for tool_call in message.tool_calls
                ],
            }
        )

        # ----------------------------------------------------
        # Execute requested tools.
        # ----------------------------------------------------

        for tool_call in message.tool_calls:

            function_name = tool_call.function.name

            arguments = json.loads(
                tool_call.function.arguments or "{}"
            )

            print(
                f"\nAgent -> {function_name}"
            )

            if arguments:
                print(
                    f"Arguments -> {arguments}"
                )

            # Find Python function
            function = AVAILABLE_FUNCTIONS.get(
                function_name
            )

            if not function:

                result = (
                    f"ERROR: Unknown tool "
                    f"'{function_name}'"
                )

            else:

                try:

                    result = function(**arguments)

                except Exception as exc:

                    result = (
                        f"ERROR executing "
                        f"{function_name}: {exc}"
                    )

            print(
                f"Result -> {result}\n"
            )

            # ------------------------------------------------
            # Give tool result back to OpenAI.
            # ------------------------------------------------

            history.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                }
            )


# ============================================================
# Main
# ============================================================

def main():

    print(
        "Git Agent"
    )

    print(
        "Type: 'commit my code to GitHub'"
    )

    print(
        "Type 'exit' to quit.\n"
    )

    history = []

    while True:

        try:

            user_input = input("You: ").strip()

        except (
            KeyboardInterrupt,
            EOFError,
        ):

            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in {
            "exit",
            "quit",
        }:

            print("Goodbye!")
            break

        history = run_agent(
            user_input,
            history,
        )


if __name__ == "__main__":
    main()