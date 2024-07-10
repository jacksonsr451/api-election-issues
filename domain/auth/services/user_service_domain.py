import uuid
from typing import Dict

from domain.auth.entities.user import UserEntity
from domain.auth.services.password_encryption_service import (
    PasswordEncryptionService,
)


class UserServiceDomain:
    @staticmethod
    def create_user(email: str, password: str) -> UserEntity:
        id: str = str(uuid.uuid4())
        password = PasswordEncryptionService.encrypt_password(
            password=password
        )
        return UserEntity(id=id, email=email, password=password)

    @staticmethod
    def update_user(id: str, email: str) -> UserEntity:
        user = UserEntity(id=id, email=email)
        del user['password']
        return user

    @staticmethod
    def update_password(id: str, password: str) -> UserEntity:
        password = PasswordEncryptionService.encrypt_password(
            password=password
        )
        return UserEntity(id=id, password=password)
