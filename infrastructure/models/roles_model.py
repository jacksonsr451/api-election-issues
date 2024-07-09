from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, backref

from infrastructure.models.base_model_sql import BaseModelSQL


class RolesModel(BaseModelSQL):
    __tablename__ = 'roles'

    name = Column(String, nullable=False)

    permissions = relationship(
        'PermissionModel',
        secondary='role_permission',
        backref=backref('roles', lazy='dynamic')
    )
    users = relationship('UsersModel', secondary='user_role')
