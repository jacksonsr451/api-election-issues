from sqlalchemy import UUID, Column, ForeignKey, Text
from sqlalchemy.orm import MappedColumn, relationship

from infrastructure.models.base_model_sql import BaseModelSQL


class AnswersModel(BaseModelSQL):
    __tablename__ = 'answers'

    device_location: MappedColumn[str] = Column(Text, nullable=True)
    issue_id: MappedColumn[str] = Column(
        UUID(as_uuid=True), ForeignKey('election_issues.id'), nullable=False
    )
    user_id: MappedColumn[str] = Column(
        UUID(as_uuid=True), ForeignKey('users.id'), nullable=False
    )
    interviewed_id: MappedColumn[str] = Column(
        UUID(as_uuid=True), ForeignKey('interviewed.id'), nullable=False
    )
    questions_answers_id: MappedColumn[str] = Column(
        UUID(as_uuid=True), ForeignKey('questions_answers.id'), nullable=False
    )

    election_issue = relationship(
        'ElectionIssuesModel', back_populates='answer'
    )
    user = relationship('UsersModel', back_populates='answer')
    interviewed = relationship('InterviewedModel', back_populates='answer')
    questions_answer = relationship(
        'QuestionsAnswersModel', back_populates='answer'
    )
