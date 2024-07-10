from sqlalchemy.orm import joinedload, subqueryload

from infrastructure.models import PermissionModel, RolesModel, UsersModel
from infrastructure.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, model: UsersModel):
        BaseRepository.__init__(self, model=model)

    def get_all(self) -> list:
        return (
            self.db.query(UsersModel)
            .options(
                joinedload(UsersModel.roles).joinedload(RolesModel.permissions)
            )
            .all()
        )
