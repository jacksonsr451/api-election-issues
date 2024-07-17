from domain.answers.answers_entity import AnswersEntity, Interviewed
from infrastructure.exceptions.database_exception import DatabaseException
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
        try:
            data_answers = data.model_dump()

            interview_data = data_answers['interviewed']
            del data_answers['interviewed']

            questions_data = data_answers['questions_answers']
            del data_answers['questions_answers']

            instance_interviewed = InterviewedModel(**interview_data)
            self.db.add(instance_interviewed)

            instance_answers = AnswersModel(**data_answers)
            instance_answers.interviewed_id = instance_interviewed.id

            for question_data in questions_data:
                instance_questions = QuestionsAnswersModel(**question_data)
                instance_answers.questions_answers.append(instance_questions)
                self.db.add(instance_questions)

            self.db.add(instance_answers)
            return self._extracted_from_update_5(instance_answers)
        except Exception as e:
            name = AnswersModel.__name__.replace('Model', '')
            raise DatabaseException(
                message=f'{e} with id {id} not found', status_code=404
            ) from e