from pydantic import Field, BaseModel
from typing import Annotated

class ChatRequest(BaseModel):
    user_query: Annotated[str, Field(..., description="Ask AI..")]