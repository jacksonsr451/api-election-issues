from domain.answers.answers_entity import AnswersEntity, Interviewed
from infrastructure.models import (
    AnswersModel,
    ElectionIssuesModel,
    InterviewedModel,
    QuestionsAnswersModel,
    UsersModel,
)
from infrastructure.repositories.base_repository import BaseRepository


class AnswersRepository(BaseRepository):
    def __init__(self, model: AnswersModel):
        super().__init__(model=model)

    def create(self, data: AnswersEntity) -> AnswersModel | None:
        data_answers = data.model_dump()

        election_issue_id = data_answers.get('issue_id')
        del data_answers['issue_id']

        instance_election_issue = (
            self.db.query(ElectionIssuesModel)
            .filter_by(id=election_issue_id)
            .first()
        )
        if not instance_election_issue:
            raise ValueError('Instance of election issue not found')

        user_id = data_answers.get('user_id')
        del data_answers['user_id']

        instance_user = self.db.query(UsersModel).filter_by(id=user_id)
        if not instance_user:
            raise ValueError('Instance of user not found')

        interviewed_data = data_answers.get('interviewed')
        del data_answers['interviewed']

        instance_interviewed = InterviewedModel(**interviewed_data)

        questions_answers_data = data_answers.get('questions_answers')
        del data_answers['questions_answers']

        instance_answers = AnswersModel(**data_answers)

        instance_answers.interviewed.append(instance_interviewed)

        for question_answers_data in questions_answers_data:
            instance_questions_answers = QuestionsAnswersModel(
                **question_answers_data
            )
            instance_answers.questions_answer.append(
                instance_questions_answers
            )

        self.db.add(instance_answers)
        return self._extracted_from_update_5(instance_answers)
