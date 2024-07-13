from typing import List, Optional

from domain.election_issues.entities.election_issue_entity import (
    ElectionIssuesEntity,
    OptionsEntity,
    QuestionsEntity,
)


class ElectionIssuesDomainService:
    __id: str
    __type: str
    __title: str
    __location: str
    __year: int
    __questions: Optional[List[QuestionsEntity[List[OptionsEntity]]]]

    def __init__(self, election_issues: ElectionIssuesEntity) -> None:
        data = election_issues.model_dump()
        self.__id = data.get('id')
        self.__type = data.get('type')
        self.__title = data.get('title')
        self.__location = data.get('location')
        self.__year = data.get('year')
        self.__questions = data.get('questions')


