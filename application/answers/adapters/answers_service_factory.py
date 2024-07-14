from application.answers.services.answers_service import AnswersService
from infrastructure.models import AnswersModel
from infrastructure.repositories.answers_repository import AnswersRepository


def get_answers_service() -> AnswersService:
    repository = AnswersRepository(AnswersModel)
    return AnswersService(repository)
