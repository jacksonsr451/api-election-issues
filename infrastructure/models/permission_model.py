from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from infrastructure.models.base_model_sql import BaseModelSQL
from infrastructure.models.role_permission_model import role_permission_table


class PermissionModel(BaseModelSQL):
    __tablename__ = 'permissions'

    name = Column(String(50), unique=True, nullable=False)

    roles = relationship(
        'RolesModel',
        secondary=role_permission_table,
        back_populates='permissions',
    )
