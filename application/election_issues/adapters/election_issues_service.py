from application.election_issues.services.election_issues_service import (
    ElectionIssuesService,
)
from infrastructure.models import ElectionIssuesModel
from infrastructure.repositories.election_issues_repository import (
    ElectionIssuesRepository,
)


def get_election_issues_service():
    repository = ElectionIssuesRepository(ElectionIssuesModel)
    return ElectionIssuesService(repository)
