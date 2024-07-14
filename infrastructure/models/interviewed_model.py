from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import MappedColumn, relationship

from infrastructure.models import BaseModelSQL


class InterviewedModel(BaseModelSQL):
    __tablename__ = 'interviewed'

    profession: MappedColumn[str] = Column(String, nullable=False)
    age: MappedColumn[int] = Column(Integer, nullable=False)
    marital_status: MappedColumn[str] = Column(String, nullable=False)
    gender: MappedColumn[str] = Column(String, nullable=False)
    education_level: MappedColumn[str] = Column(String, nullable=False)
    neighborhood: MappedColumn[str] = Column(String, nullable=False)
    household_income: MappedColumn[str] = Column(String, nullable=False)
    own_house: MappedColumn[str] = Column(String, nullable=False)
    religion: MappedColumn[str] = Column(String, nullable=False)

    answer = relationship(
        'AnswersModel',
        back_populates='interviewed',
        cascade='all, delete-orphan',
        lazy='dynamic',
    )
