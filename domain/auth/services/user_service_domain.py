import uuid

from pydantic import BaseModel

from domain.auth.entities.user import User
from domain.auth.services.password_encryption_service import (
    PasswordEncryptionService,
)


class UserServiceDomain:
    @staticmethod
    def create_user(email: str, password: str) -> BaseModel:
        """

        :rtype: object
        """
        id: str = str(uuid.uuid4())
        password = PasswordEncryptionService.encrypt_password(
            password=password
        )
        user = User(_id=id, email=email, password=password)
        return user.get()

    @staticmethod
    def update_user(id: str, email: str) -> BaseModel:
        user_updated = User(_id=id, email=email)
        user = user_updated.get()
        del user['password']
        return user

    @staticmethod
    def update_password(id: str, password: str) -> BaseModel:
        password = PasswordEncryptionService.encrypt_password(
            password=password
        )
        user = User(_id=id, password=password)
        return user.get()

    # @staticmethod
    # def check_permission(user_id, permission_name):
    #     user = User.query.get(user_id)
    #     if user and any(permission.name == permission_name for role in user.roles for permission in role.permissions):
    #         return jsonify({"result": True})
    #     return jsonify({"result": False})
