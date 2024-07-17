from typing import List, Optional
from uuid import uuid4

from pydantic import UUID4, BaseModel, Field


class OptionsEntity(BaseModel):
    id: Optional[UUID4 | str] = Field(default_factory=uuid4)
    text: str = Field(default='')

    def __init__(self, **data):
        super().__init__(**data)
        if not self.id:
            self.id = uuid4()

class QuestionsEntity(BaseModel):
    id: Optional[UUID4 | str] = Field(default_factory=uuid4)
    text: str = Field(default='')
    options: Optional[List[OptionsEntity]] = Field(default=[])

    def __init__(self, **data):
        super().__init__(**data)
        if not self.id:
            self.id = uuid4()

class ElectionIssuesEntity(BaseModel):
    id: Optional[UUID4 | str] = Field(default_factory=uuid4)
    type: str = Field(default='election_issue')
    title: str = Field(default='')
    location: str = Field(default='')
    year: int = Field(default=2022)
    questions: Optional[List[QuestionsEntity]] = Field(default=[])

    def __init__(self, **data):
        super().__init__(**data)
        if not self.id:
            self.id = uuid4()
