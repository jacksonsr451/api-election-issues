from sqlalchemy import Column, ForeignKey, Text, UUID, Table
from sqlalchemy.orm import relationship
from infrastructure.models.base_model_sql import BaseModelSQL


answers_questions = Table(
    'answers_questions',
    BaseModelSQL.metadata,
    Column('answers_id', UUID(as_uuid=True), ForeignKey('answers.id')),
    Column('questions_answers_id', UUID(as_uuid=True), ForeignKey('questions_answers.id')),
)


class AnswersModel(BaseModelSQL):
    __tablename__ = 'answers'

    device_location = Column(Text, nullable=True)
    issue_id = Column(UUID(as_uuid=True), ForeignKey('election_issues.id'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    interviewed_id = Column(UUID(as_uuid=True), ForeignKey('interviewed.id'), nullable=False)

    election_issue = relationship('ElectionIssuesModel', back_populates='answer')
    user = relationship('UsersModel', back_populates='answer')
    interviewed = relationship('InterviewedModel', back_populates='answer')

    questions_answers = relationship(
        'QuestionsAnswersModel',
        secondary=answers_questions,
        back_populates='answers',
    )
