from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from infrastructure.models.base_model_sql import BaseModelSQL
from infrastructure.models.user_role_model import role_user_table


class UsersModel(BaseModelSQL):
    __tablename__ = 'users'

    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    roles = relationship("RolesModel", secondary=role_user_table, back_populates="users")
