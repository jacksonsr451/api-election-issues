from sqlalchemy import Column, ForeignKey, Text, UUID, CheckConstraint
from sqlalchemy.orm import relationship, validates
from infrastructure.models.base_model_sql import BaseModelSQL
from infrastructure.models.answers_model import answers_questions

class QuestionsAnswersModel(BaseModelSQL):
    __tablename__ = 'questions_answers'

    question_id = Column(UUID(as_uuid=True), ForeignKey('questions.id'), nullable=False)
    option_id = Column(UUID(as_uuid=True), ForeignKey('options.id'), nullable=True)
    response = Column(Text, nullable=True)

    question = relationship('QuestionsModel', back_populates='answer')
    option_answer = relationship('OptionsModel', back_populates='answer')

    answers = relationship(
        'AnswersModel',
        secondary=answers_questions,
        back_populates='questions_answers',
    )

    __table_args__ = (
        CheckConstraint(
            '(option_id IS NOT NULL AND response IS NULL) OR (option_id IS NULL AND response IS NOT NULL)',
            name='option_or_response_check',
        ),
    )

    @validates('option_id', 'response')
    def validate_option_or_response(self, key, value):
        if key == 'option_id':
            if value is not None and self.response is not None:
                raise ValueError('Both option_id and response cannot be set simultaneously.')
        elif key == 'response':
            if value is not None and self.option_id is not None:
                raise ValueError('Both option_id and response cannot be set simultaneously.')
        return value
