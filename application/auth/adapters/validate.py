from fastapi import HTTPException

from infrastructure.models import UsersModel


class Validate:
    @staticmethod
    def validate_role(user: UsersModel, role: str):
        if all(r.name != role for r in user.roles):
            raise HTTPException(
                status_code=404, detail=f'Role "{role}" not found.'
            )

    @staticmethod
    def validate_permissions(user: UsersModel, permission: str):
        for role in user.roles:
            if any(p.name == permission for p in role.permissions):
                return
        raise HTTPException(
            status_code=404, detail=f'Permission "{permission}" not found.'
        )


def get_validate() -> Validate:
    return Validate
