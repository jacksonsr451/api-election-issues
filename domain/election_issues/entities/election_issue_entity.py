from typing import Optional, List
from uuid import uuid4

from pydantic import BaseModel, Field, UUID4


class OptionsEntity(BaseModel):
    index: UUID4 = Field(default=uuid4())
    text: str = Field(default="")


class QuestionsEntity(BaseModel):
    index: UUID4 = Field(default=uuid4())
    text: str = Field(default="")
    options: Optional[List[OptionsEntity]] = Field(default=[])


class ElectionIssuesEntity(BaseModel):
    index: UUID4 = Field(default=uuid4())
    type: str = Field(default="election_issue")
    title: str = Field(default="")
    location: str = Field(default="")
    year: int = Field(default=2022)
    questions: Optional[List[Questions]] = Field(default=[])
