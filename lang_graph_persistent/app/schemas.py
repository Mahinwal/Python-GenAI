from pydantic import BaseModel, Field
from typing import Annotated

class ChatRequest(BaseModel):
    thread_id: Annotated[str, Field(..., description="Conversation/session identifier")]
    message: Annotated[str, Field(..., min_length=2)]


class ChatResponse(BaseModel):
    thread_id: str
    reply: str
    message_count: int