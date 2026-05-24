from typing import List

from pydantic import BaseModel, Field


class Mcq(BaseModel):
    question: str
    wrong_answer: List[str] = Field(description="wrong answer option")
    right_answer: str = Field(description="right answer option")
    explanation: str


class UserQuestionOut(BaseModel):
    mcq: List[Mcq]
