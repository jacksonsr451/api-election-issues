from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import MappedColumn, relationship

from infrastructure.models.base_model_sql import BaseModelSQL


class ElectionIssuesModel(BaseModelSQL):
    __tablename__ = 'election_issues'

    type: MappedColumn[str] = Column(String(50), nullable=False)
    title: MappedColumn[str] = Column(String(255), nullable=False)
    location: MappedColumn[str] = Column(String(255), nullable=False)
    year: MappedColumn[int] = Column(Integer, nullable=False)

    questions = relationship(
        'QuestionsModel',
        back_populates='election_issue',
        cascade='all, delete-orphan',
        lazy='dynamic',
    )

    answer = relationship(
        'AnswersModel',
        back_populates='election_issue',
        cascade='all, delete-orphan',
        lazy='dynamic',
    )
