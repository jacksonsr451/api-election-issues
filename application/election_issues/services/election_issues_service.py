from fastapi import Depends

from application.election_issues.schemas.election_issues_schemas import (
    ElectionIssues,
    ElectionIssuesCreate,
    ElectionIssuesUpdate,
)
from domain.election_issues.election_issue_entity import ElectionIssuesEntity
from infrastructure.repositories.election_issues_repository import (
    ElectionIssuesRepository,
)


class ElectionIssuesService:
    def __init__(self, repository: Depends(ElectionIssuesRepository)):
        self.__repository: ElectionIssuesRepository = repository

    def create_election_issue(self, data: ElectionIssuesCreate):
        entity = ElectionIssuesEntity(**data.model_dump())
        model = self.__repository.create(entity)
        return model.to_schema(schema=ElectionIssues).model_dump()

    def update_election_issue(self, id: str, data: ElectionIssuesUpdate):
        entity = ElectionIssuesEntity(**data.model_dump())
        model = self.__repository.update(id, entity)
        return model.to_schema(schema=ElectionIssues).model_dump()

    def get_all_election_issues(self):
        return self.__repository.get_all()

    def get_election_issue(self, id: str):
        return self.__repository.get_by_id(id)

    def delete_election_issue(self, id: str):
        self.__repository.delete(id)
