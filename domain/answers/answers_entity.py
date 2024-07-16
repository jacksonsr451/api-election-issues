from enum import Enum
from typing import List, Optional
from uuid import uuid4

from pydantic import UUID4, BaseModel, Field


class QuestionsAnswers(BaseModel):
    id: Optional[UUID4 | str] = Field(default_factory=uuid4)
    question_id: str = Field(...)
    option_id: Optional[str] = Field(default=None)
    response: Optional[str] = Field(default=None)

    def __init__(self, **data):
        super().__init__(**data)
        if not self.id:
            self.id = uuid4()

class Interviewed(BaseModel):
    id: Optional[UUID4 | str] = Field(default_factory=uuid4)
    profession: str = Field(..., min_length=1)
    age: int = Field(..., ge=0)
    marital_status: str = Field(...)
    gender: str = Field(...)
    education_level: str = Field(...)
    neighborhood: str = Field(..., min_length=1)
    household_income: str = Field(...)
    own_house: str = Field(...)
    religion: str = Field(..., min_length=1)

    def __init__(self, **data):
        super().__init__(**data)
        if not self.id:
            self.id = uuid4()

class AnswersEntity(BaseModel):
    id: Optional[UUID4 | str] = Field(default_factory=uuid4)
    device_location: str = Field(...)
    issue_id: str = Field(...)
    user_id: str = Field(...)
    interviewed: Interviewed = Field(...)
    questions_answers: List[QuestionsAnswers] = Field(...)

    def __init__(self, **data):
        super().__init__(**data)
        if not self.id:
            self.id = uuid4()
