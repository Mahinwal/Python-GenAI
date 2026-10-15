from typing import TypedDict, Annotated

from langgraph.graph.message import add_messages
from langgraph.graph.state import StateGraph, START, END
from langchain_openai import ChatOpenAI

from app.config import get_settings

class State(TypedDict):
    messages: Annotated[list, add_messages]


def get_llm():
    settings = get_settings()
    return ChatOpenAI(model=settings.OPENAI_MODEL, api_key=settings.OPENAI_API_KEY)


def chat(state: State):
    response = get_llm().invoke(state["messages"])
    return {"messages": [response]}


def build_graph(checkpointer):
    builder = StateGraph(State)

    builder.add_node("chat", chat)
    builder.add_edge(START, "chat")
    builder.add_edge("chat", END)

    return builder.compile(checkpointer=checkpointer)


