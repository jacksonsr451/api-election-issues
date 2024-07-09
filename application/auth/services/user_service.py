from typing import List

from infrastructure.models.users_model import UsersModel
from infrastructure.repositories.user_repository import UserRepository
from application.auth.schemas.user_schema import UserCreate, UserUpdate, UpdateUserPassword, UserSchema
from domain.auth.services.user_service_domain import UserServiceDomain


class UserService:
    def __init__(self, repository: UserRepository):
        self.__repository = repository

    def create_user(self, user: UserCreate) -> UserSchema:
        data: UserCreate = UserServiceDomain.create_user(**user.model_dump())
        user_model: UsersModel = self.__repository.create(data)
        return user_model.to_schema(UserSchema)

    def update_user(self, _id: str, user: UserUpdate) -> UserSchema:
        data: UserUpdate = UserServiceDomain.update_user(**user.model_dump())
        user_model: UsersModel = self.__repository.update(_id, data)
        return user_model.to_schema(UserSchema)

    def update_password(self, _id: str, user: UpdateUserPassword) -> UserSchema:
        data: UserUpdate = UserServiceDomain.update_password(**user.model_dump())
        user_model: UsersModel = self.__repository.update(_id, data)
        return user_model.to_schema(UserSchema)

    def get_user(self, _id: str) -> UserSchema:
        user_model = self.__repository.get_by_id(_id)
        return user_model.to_schema(UserSchema)

    def get_all_users(self) -> List[UserSchema]:
        users = self.__repository.get_all()
        return [user.to_schema(UserSchema) for user in users]

    def delete_user(self, _id: str) -> None:
        self.__repository.delete(_id)