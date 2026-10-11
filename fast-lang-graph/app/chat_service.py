from openai import OpenAI

from typing import Literal
from langgraph.graph import StateGraph, START, END

from app.schemas import AgentState, ClassifyMessageResponse, CodeAccuracyResponse
from app.config import Config

config = Config()

client = OpenAI(
    api_key=config.OPENAI_API_KEY.get_secret_value()
)


# Nodes

async def classify(state: AgentState):
    user_query = state["user_query"]

    SYSTEM_PROMPT = """
        You are an AI assistant. Your job is to detect if the user's query is
        related to coding question or not.
        Return the response in specified JSON boolean only.
        """

    response = client.beta.chat.completions.parse(
        model=config.OPENAI_MODEL_NANO,
        response_format=ClassifyMessageResponse,
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



async def general_query(state: AgentState):
    user_query = state["user_query"]

    response = client.chat.completions.create(
        model=config.OPENAI_MODEL_MINI,
        messages=[
            {"role": "user", "content": user_query}
        ]
    )

    llm_result = response.choices[0].message.content

    return {
        "llm_result": llm_result or ""
    }


async def coding_query(state: AgentState):
    user_query = state["user_query"]

    SYSTEM_PROMPT = """
        You are an expert Python developer.
    
        Answer coding questions with:
        1. A clear explanation.
        2. Correct and readable code.
        3. An explanation of the code.
        4. Time and space complexity when relevant.
        """

    response = client.chat.completions.create(
        model=config.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query}
        ]
    )

    llm_result = response.choices[0].message.content

    return {
        "llm_result": llm_result or ""
    }


async def evaluate(state: AgentState):
    user_query = state["user_query"]
    llm_code = state["llm_result"]

    SYSTEM_PROMPT = f"""
            You are expert in calculating accuracy of the code according to the question.
            Return the percentage of accuracy
            
            User Query: {user_query}
            Code: {llm_code}
        """

    response = client.beta.chat.completions.parse(
        model=config.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query}
        ],
        response_format=CodeAccuracyResponse
    )

    parsed = response.choices[0].message.parsed

    if parsed is None:
        raise ValueError("Could not evaluate the generated answer")
    
    return {
        "accuracy_percentage": parsed.accuracy_percentage
    }


async def route_query(state: AgentState) -> Literal["general_query", "coding_query"]:
    if state["is_coding_question"]:
        return "coding_query"
    
    return "general_query"


def builder():
    # Build the graph
    graph_builder = StateGraph(AgentState)
    graph_builder.add_node("classify", classify)
    graph_builder.add_node("general_query", general_query)
    graph_builder.add_node("coding_query", coding_query)
    graph_builder.add_node("evaluate", evaluate)

    graph_builder.add_edge(START, "classify")
    graph_builder.add_conditional_edges(
        "classify", route_query
    )
    graph_builder.add_edge("general_query", END)
    graph_builder.add_edge("coding_query", "evaluate")
    graph_builder.add_edge("evaluate", END)

    return graph_builder.compile()
