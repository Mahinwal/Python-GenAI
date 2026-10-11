from typing import TypedDict
from pydantic import BaseModel


class AgentState(TypedDict):
    query: str
    llm_result: str | None
    is_coding_question: bool
    accuracy_percentage: float | None


class ClassifyMessageResponse(BaseModel):
    is_coding_question: bool


class CodeAccuracyResponse(BaseModel):
    accuracy_percentage: float