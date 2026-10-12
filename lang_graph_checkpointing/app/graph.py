from functools import lru_cache
from typing import TypedDict, Annotated

from langgraph.graph.message import add_messages
from langgraph.graph.state import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

from openai import OpenAI

from app.config import get_settings

settings = get_settings()

client = OpenAI(
    api_key=settings.OPENAI_API_KEY.get_secret_value()
)

role_map = {"human": "user", "ai": "assistant", "system": "system"}

class State(TypedDict):
    messages: Annotated[list, add_messages]


def chatbot(state: State):
    openai_messages = [
        {"role": role_map.get(m.type, m.type), "content": m.content}
        for m in state["messages"]
    ]

    response = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=openai_messages,
    )

    return {"messages": [("assistant", response.choices[0].message.content)]}


def build_graph():
    builder = StateGraph(State)

    builder.add_node("chatbot", chatbot)
    builder.add_edge(START, "chatbot")
    builder.add_edge("chatbot", END)

    checkPointer = InMemorySaver()

    return builder.compile(checkpointer=checkPointer)


@lru_cache
def get_graph():
    return build_graph()
