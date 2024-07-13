from infrastructure.models import BaseModelSQL
from infrastructure.models.election_issues_model import ElectionIssuesModel


class ElectionIssuesRepository(ElectionIssuesModel):
    def __init__(self, model: BaseModelSQL):
        super().__init__(model=model)
