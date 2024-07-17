from typing import List, Optional

from pydantic import BaseModel, Field


class QuestionsAnswersBase(BaseModel):
    question_id: str
    option_id: Optional[str] = Field(default=None)
    response: Optional[str] = Field(default=None)


class QuestionsAnswersCreate(QuestionsAnswersBase):
    pass


class QuestionsSchema(BaseModel):
    id: str
    question_id: str
    option_id: Optional[str] = Field(default=None)
    response: Optional[str] = Field(default=None)


class InterviewedBase(BaseModel):
    profession: str
    age: int
    marital_status: str
    gender: str
    education_level: str
    neighborhood: str
    household_income: str
    own_house: str
    religion: str


class InterviewedCreate(InterviewedBase):
    pass


class InterviewedSchema(BaseModel):
    id: str
    profession: str
    age: int
    marital_status: str
    gender: str
    education_level: str
    neighborhood: str
    household_income: str
    own_house: str
    religion: str


class AnswersBase(BaseModel):
    device_location: str
    issue_id: str
    user_id: str


class AnswersCreate(AnswersBase):
    interviewed: Optional[InterviewedCreate] = Field(default=None)
    questions_answers: Optional[List[QuestionsAnswersCreate]] = Field(
        default=[]
    )


class AnswersSchema(BaseModel):
    id: str
    device_location: str
    issue_id: str
    user_id: str
    interviewed: Optional[InterviewedCreate] = Field(default=None)
    questions_answers: Optional[List[QuestionsAnswersCreate]] = Field(
        default=[]
    )
