from typing import List, Any, Dict

from fastapi import HTTPException

from application.auth.schemas.user_schema import (
    UpdateUserPassword,
    UserCreate,
    UserSchema,
    UserUpdate,
)
from domain.auth.services.password_encryption_service import (
    PasswordEncryptionService,
)
from domain.auth.user_entity import UserEntity
from infrastructure.models.users_model import UsersModel
from infrastructure.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.__repository = repository

    def create_user(self, user: UserCreate) -> Dict[str, Any]:
        data: UserEntity = UserEntity(**user.model_dump())
        user_model: UsersModel = self.__repository.create(data)
        return user_model.to_schema(UserSchema).model_dump()

    def update_user(self, _id: str, user: UserUpdate) -> Dict[str, Any]:
        data: UserEntity = UserEntity(**user.model_dump())
        user_model: UsersModel | None = self.__repository.update(_id, data)
        return user_model.to_schema(UserSchema).model_dump()

    def update_password(
        self, _id: str, user: UpdateUserPassword
    ) -> Dict[str, Any]:
        data: UserEntity = UserEntity(**user.model_dump())
        user_model: UsersModel | None = self.__repository.update(_id, data)
        return user_model.to_schema(UserSchema).model_dump()

    def get_user(self, _id: str) -> Dict[str, Any]:
        user_model = self.__repository.get_by_id(_id)
        return user_model.to_schema(UserSchema).model_dump()

    def get_all_users(self) -> List[Dict[str, Any]]:
        users = self.__repository.get_all()
        return [user.to_schema(UserSchema).model_dump() for user in users]

    def delete_user(self, _id: str) -> None:
        self.__repository.delete(_id)

    def login(self, email: str, password: str) -> UserSchema:
        user: UsersModel = self.__repository.get_user_by_email(email)
        if not user or not PasswordEncryptionService.verify_password(
            password, user.password
        ):
            raise HTTPException(
                status_code=401, detail='Incorrect email or password'
            )
        return user.to_schema(UserSchema)
