from sqlalchemy import Column, UUID, ForeignKey

from infrastructure.models.base_model_sql import BaseModelSQL


class UserRoleModel(BaseModelSQL):
    __tablename__ = 'user_role'

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    role_id = Column(UUID(as_uuid=True), ForeignKey('roles.id'))
