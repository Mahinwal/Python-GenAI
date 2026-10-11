from fastapi import APIRouter, Query
from typing import Annotated
from app.service_graph import builder
from app.schemas import AgentState

router = APIRouter(prefix="", tags=["Chat"])


@router.get("/chat")
async def chat(
    query: Annotated[str, Query(description="Ask AI")]
):
    initial_state: AgentState = {
        "query": query,
        "llm_result": None,
        "is_coding_question": False,
        "accuracy_percentage": None,
    }

    graph = builder()

    response = await graph.ainvoke(initial_state)

    return {
        "query": response["query"],
        "is_coding_question": response["is_coding_question"],
        "result": response["llm_result"],
        "accuracy_percentage": response["accuracy_percentage"],
    }