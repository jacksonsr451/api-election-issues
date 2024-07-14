from email.policy import default
from typing import List, Optional
from uuid import uuid4

from pydantic import UUID4, BaseModel, Field


class OptionsBase(BaseModel):
    text: str = Field(default='')


class OptionsCreate(OptionsBase):
    pass


class OptionsUpdate(OptionsBase):
    id: Optional[str] = Field(default=None)
    pass


class Options(BaseModel):
    id: str
    text: str
    created_at: str
    updated_at: str


class QuestionsBase(BaseModel):
    text: str = Field(default='')


class QuestionsCreate(QuestionsBase):
    options: Optional[List[OptionsCreate]] = Field(default=[])


class QuestionsUpdate(QuestionsBase):
    id: Optional[str] = Field(default=None)
    options: Optional[List[OptionsUpdate]] = Field(default=[])


class Questions(BaseModel):
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


class ElectionIssuesCreate(ElectionIssuesBase):
    questions: Optional[List[QuestionsCreate]] = Field(default=[])


class ElectionIssuesUpdate(ElectionIssuesBase):
    questions: Optional[List[QuestionsUpdate]] = Field(default=[])


class ElectionIssues(BaseModel):
    id: str
    type: str
    title: str
    location: str
    year: int
    questions: Optional[List[Questions]] = Field(default=[])
    created_at: str
    updated_at: str
