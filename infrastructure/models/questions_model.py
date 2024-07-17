from sqlalchemy import UUID, Column, ForeignKey, String
from sqlalchemy.orm import MappedColumn, relationship

from infrastructure.models.base_model_sql import BaseModelSQL


class QuestionsModel(BaseModelSQL):
    __tablename__ = 'questions'

    text: MappedColumn[str] = Column(String(255), nullable=False)

    election_issues_id: MappedColumn[str] = Column(
        UUID(as_uuid=True),
        ForeignKey('election_issues.id'),
        nullable=False,
    )

    election_issue = relationship('ElectionIssuesModel', back_populates='questions')
    options = relationship('OptionsModel', back_populates='question')

    answer = relationship(
        'QuestionsAnswersModel',
        back_populates='question',
        cascade='all, delete-orphan',
        lazy='dynamic',
    )
