from typing import List, Optional
from uuid import uuid4

from pydantic import UUID4, BaseModel, Field


class OptionsEntity(BaseModel):
    id: UUID4 = Field(default=uuid4())
    text: str = Field(default='')


class QuestionsEntity(BaseModel):
    id: UUID4 = Field(default=uuid4())
    text: str = Field(default='')
    options: Optional[List[OptionsEntity]] = Field(default=[])


class ElectionIssuesEntity(BaseModel):
    id: UUID4 = Field(default=uuid4())
    type: str = Field(default='election_issue')
    title: str = Field(default='')
    location: str = Field(default='')
    year: int = Field(default=2022)
    questions: Optional[List[Questions]] = Field(default=[])
