from dotenv import load_dotenv
from typing import Literal
from app.schemas import AgentState, ClassifyMessageResponse, CodeAccuracyResponse
from langgraph.graph import StateGraph, START, END
from openai import OpenAI

load_dotenv()


client = OpenAI()


async def classify_message(state: AgentState):
    user_query = state["query"]

    SYSTEM_PROMPT = """
    You are an AI assistant. Your job is to detect if the user's query is
    related to coding question or not.
    Return the response in specified JSON boolean only.
    """

    response = client.beta.chat.completions.parse(
        model="gpt-4.1-nano",
        response_format= ClassifyMessageResponse,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query}
        ]
    )

    parsed = response.choices[0].message.parsed

    if parsed is None:
        raise ValueError("Could not classify the user query")

    return {
        "is_coding_question": parsed.is_coding_question
    }


async def route_query(state: AgentState) -> Literal["simple_query", "coding_query"]:
    if state["is_coding_question"]:
        return "coding_query"

    return "simple_query"


async def simple_query(state: AgentState):
    query = state["query"]

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": query}
        ]
    )

    content = response.choices[0].message.content

    return {
        "llm_result": content or ""
    }


async def coding_query(state: AgentState):
    query = state["query"]

    SYSTEM_PROMPT = """
    You are an expert Python developer.

    Answer coding questions with:
    1. A clear explanation.
    2. Correct and readable code.
    3. An explanation of the code.
    4. Time and space complexity when relevant.
    """


    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ]
    )

    content = response.choices[0].message.content

    return {
        "llm_result": content or ""
    }



async def evaluate_query(state: AgentState):
    query = state["query"]

    llm_code = state["llm_result"]

    SYSTEM_PROMPT = f"""
        You are expert in calculating accuracy of the code according to the question.
        Return the percentage of accuracy
        
        User Query: {query}
        Code: {llm_code}
    """

    response = client.beta.chat.completions.parse(
        model="gpt-4.1",
        response_format=CodeAccuracyResponse,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ]
    )

    parsed = response.choices[0].message.parsed

    if parsed is None:
        raise ValueError("Could not evaluate the generated answer")

    return {
        "accuracy_percentage": parsed.accuracy_percentage
    }


def builder():
    # Build the graph
    graph_builder = StateGraph(AgentState)

    graph_builder.add_node("classify_message", classify_message)
    graph_builder.add_node("simple_query", simple_query)
    graph_builder.add_node("coding_query", coding_query)
    graph_builder.add_node("evaluate_query", evaluate_query)

    graph_builder.add_edge(START, "classify_message")
    graph_builder.add_conditional_edges(
        "classify_message", route_query
    )
    graph_builder.add_edge("simple_query", END)
    graph_builder.add_edge("coding_query", "evaluate_query")
    graph_builder.add_edge("evaluate_query", END)

    return graph_builder.compile()
