from typing import Any, Dict, List

from application.answers.schemas.answers_schema import (
    AnswersCreate,
    AnswersSchema,
)
from domain.answers.answers_entity import AnswersEntity
from infrastructure.repositories.answers_repository import AnswersRepository


class AnswersService:
    def __init__(self, repository: AnswersRepository):
        self.__repository = repository

    def include_answer(self, data: AnswersCreate) -> Dict[str, Any]:
        entity = AnswersEntity(**data.model_dump())
        model = self.__repository.create(entity)
        return model.to_schema(AnswersSchema).model_dump()

    def get_answer(self, id: str) -> Dict[str, Any]:
        model = self.__repository.get_by_id(id)
        return model.to_schema(AnswersSchema).model_dump()

    def get_all_answers(self, issue_id: str) -> List[Dict[str, Any]]:
        models = self.__repository.get_all_with_key_and_value(
            'issue_id', issue_id
        )
        return [
            model.to_schema(AnswersSchema).model_dump() for model in models
        ]

    def delete(self, id: str) -> None:
        self.__repository.delete(id)
