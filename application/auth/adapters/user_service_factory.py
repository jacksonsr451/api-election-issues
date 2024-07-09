from infrastructure.repositories.user_repository import UserRepository
from infrastructure.models.users_model import UsersModel
from application.auth.services.user_service import UserService


def get_user_service() -> UserService:
    repository = UserRepository(UsersModel)
    return UserService(repository)
