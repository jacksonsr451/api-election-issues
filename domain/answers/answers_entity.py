from enum import Enum
from typing import List, Optional
from uuid import uuid4

from pydantic import UUID4, BaseModel, Field


class QuestionsAnswers(BaseModel):
    id: UUID4 = Field(default=uuid4())
    question_id: str = Field(...)
    option_id: Optional[str] = Field(default=None)
    response: Optional[str] = Field(default=None)


class EducationLevelEnum(Enum):
    ILLITERATE = 'Analfabeto'
    ELEMENTARY_SCHOOL_1 = 'Fundamental 1'
    ELEMENTARY_SCHOOL_2 = 'Fundamental 2'
    HIGH_SCHOOL = 'Médio'
    COLLEGE = 'Superior'


class GenderEnum(Enum):
    MALE = 'Masculino'
    FEMALE = 'Feminino'


class HouseholdIncomeEnum(Enum):
    UP_TO_3_SALARIES = 'Até 3 salários mínimos'
    ABOVE_3_SALARIES = 'Acima de 3 salários mínimos'


class OwnHouseEnum(Enum):
    YES = 'Sim'
    NO = 'Não'


class MaritalStatusEnum(Enum):
    SINGLE = 'Solteiro(a)'
    MARRIED = 'Casado(a)'
    DIVORCED = 'Divorciado(a)'
    WIDOWED = 'Viúvo(a)'
    COMMON_LAW = 'União estável'


class Interviewed(BaseModel):
    id: UUID4 = Field(default=uuid4())
    profession: str = Field(..., min_length=1)
    age: int = Field(..., ge=0)
    marital_status: MaritalStatusEnum = Field(...)
    gender: GenderEnum = Field(...)
    education_level: EducationLevelEnum = Field(...)
    neighborhood: str = Field(..., min_length=1)
    household_income: HouseholdIncomeEnum = Field(...)
    own_house: OwnHouseEnum = Field(...)
    religion: str = Field(..., min_length=1)


class AnswersEntity(BaseModel):
    id: UUID4 = Field(default=uuid4())
    device_location: str = Field(...)
    issue_id: str = Field(...)
    user_id: str = Field(...)
    interviewed: Interviewed = Field(...)
    questions_answers: List[QuestionsAnswers] = Field(...)
