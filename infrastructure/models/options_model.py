from sqlalchemy import UUID, Column, ForeignKey, String
from sqlalchemy.orm import MappedColumn, relationship

from infrastructure.models.base_model_sql import BaseModelSQL


class OptionsModel(BaseModelSQL):
    __tablename__ = 'options'

    text: str = Column(String(255), nullable=False)
    question_id: MappedColumn[int] = Column(
        UUID(as_uuid=True),
        ForeignKey('questions.id'),
        nullable=False,
    )
    question = relationship('QuestionsModel', back_populates='options')
