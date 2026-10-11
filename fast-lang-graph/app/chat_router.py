from typing import Annotated
from fastapi import APIRouter, Query

from app.schemas import AgentState
from app.chat_service import builder


router = APIRouter(prefix="", tags=["Chat"])

@router.get("/chat")
async def chat(
    user_query: Annotated[str, Query(..., description="Ask AI")]
):
    initial_state: AgentState = {
            "user_query": user_query,
            "llm_result": None,
            "is_coding_question": False,
            "accuracy_percentage": None,
        }

    graph = builder()

    response = await graph.ainvoke(initial_state)

    return {
            "user_query": response["user_query"],
            "is_coding_question": response["is_coding_question"],
            "result": response["llm_result"],
            "accuracy_percentage": response["accuracy_percentage"],
        }