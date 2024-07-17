from typing import List

from fastapi import HTTPException

from infrastructure.models import UsersModel


class Validate:
    @staticmethod
    def validate_role(user: UsersModel, roles: List[str]):
        user_roles = {r.name for r in user.roles}

        if all(role not in user_roles for role in roles):
            raise HTTPException(
                status_code=404,
                detail=f'None of the specified roles {roles} found.',
            )

    @staticmethod
    def validate_permissions(user: UsersModel, permissions: List[str]):
        user_permissions = {
            p.name for role in user.roles for p in role.permissions
        }
        if all(
            permission not in user_permissions for permission in permissions
        ):
            raise HTTPException(
                status_code=404,
                detail=f'None of the specified permissions {permissions} found.',
            )


def get_validate() -> Validate:
    return Validate
