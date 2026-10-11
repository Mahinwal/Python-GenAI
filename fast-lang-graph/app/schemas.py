from typing import TypedDict
from pydantic import BaseModel

class AgentState(TypedDict):
    user_query: str
    llm_result: str
    accuracy_percentage: str
    is_coding_question: bool


class ClassifyMessageResponse(BaseModel):
    is_coding_question: bool


class CodeAccuracyResponse(BaseModel):
    accuracy_percentage: float