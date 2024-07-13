from typing import List, Optional
from uuid import uuid4

from pydantic import UUID4, BaseModel, Field


class OptionsBase(BaseModel):
    text: str = Field(default='')


class OptionsCreate(OptionsBase):
    pass


class OptionsUpdate(OptionsBase):
    pass


class Options:
    id: str
    text: str
    created_at: str
    updated_at: str


class QuestionsBase(BaseModel):
    text: str = Field(default='')
    options: Optional[List[Options]] = Field(default=[])


class QuestionsCreate(QuestionsBase):
    pass


class QuestionsUpdate(QuestionsBase):
    pass


class Questions:
    id: str
    text: str
    options: Optional[List[Options]] = Field(default=[])
    created_at: str
    updated_at: str


class ElectionIssuesBase(BaseModel):
    type: str
    title: str
    location: str
    year: int
    questions: Optional[List[Options]] = Field(default=[])


class ElectionIssuesCreate(ElectionIssuesBase):
    pass

class ElectionIssuesUpdate(ElectionIssuesBase):
    pass

class ElectionIssues:
    id: str
    type: str
    title: str
    location: str
    year: int
    questions: Optional[List[Options]] = Field(default=[])
    created_at: str
    updated_at: str
