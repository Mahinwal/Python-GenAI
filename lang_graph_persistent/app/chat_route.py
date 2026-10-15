from fastapi import APIRouter, Request
from app.schemas import ChatRequest, ChatResponse


router = APIRouter(prefix="", tags=["Chat"])

@router.post("/chat")
async def send_message(
    payload: ChatRequest,
    request: Request
):
    graph = request.app.state.graph
    config = {"configurable": {"thread_id": payload.thread_id}}
    result = graph.invoke({"messages": [("user", payload.message)]}, config)

    return ChatResponse(
        thread_id=payload.thread_id,
        reply=result["messages"][-1].content,
        message_count=len(result["messages"]),
    )


