from application.auth.services.user_service import UserService
from infrastructure.models.users_model import UsersModel
from infrastructure.repositories.user_repository import UserRepository


def get_user_service() -> UserService:
    repository = UserRepository(UsersModel)
    return UserService(repository)
