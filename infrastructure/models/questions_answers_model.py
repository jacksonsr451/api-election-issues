from sqlalchemy import UUID, CheckConstraint, Column, ForeignKey, Text
from sqlalchemy.orm import MappedColumn, relationship, validates

from infrastructure.models import BaseModelSQL


class QuestionsAnswersModel(BaseModelSQL):
    __tablename__ = 'questions_answers'

    question_id: MappedColumn[str] = Column(
        UUID(as_uuid=True), ForeignKey('questions.id'), nullable=False
    )
    option_id: MappedColumn[str] = Column(
        UUID(as_uuid=True), ForeignKey('options.id'), nullable=True
    )
    response: MappedColumn[str] = Column(Text, nullable=True)

    question = relationship(
        'QuestionsModel',
        back_populates='answer',
        cascade='all, delete-orphan',
        lazy='dynamic',
    )

    option = relationship(
        'OptionsModel',
        back_populates='answer',
        cascade='all, delete-orphan',
        lazy='dynamic',
    )

    answer = relationship(
        'AnswersModel',
        back_populates='questions_answer',
        cascade='all, delete-orphan',
        lazy='dynamic',
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
                raise ValueError(
                    'Both option_id and response cannot be set simultaneously.'
                )
        elif key == 'response':
            if value is not None and self.option_id is not None:
                raise ValueError(
                    'Both option_id and response cannot be set simultaneously.'
                )
        return value
