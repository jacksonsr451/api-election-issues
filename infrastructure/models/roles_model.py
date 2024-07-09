from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from infrastructure.models.base_model_sql import BaseModelSQL
from infrastructure.models.role_permission_model import role_permission_table
from infrastructure.models.user_role_model import role_user_table


class RolesModel(BaseModelSQL):
    __tablename__ = 'roles'

    name = Column(String, nullable=False)

    permissions = relationship('PermissionModel', secondary=role_permission_table, back_populates='roles')
    users = relationship('UsersModel', secondary=role_user_table, back_populates='roles')
