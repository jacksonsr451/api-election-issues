from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from infrastructure.models.base_model_sql import BaseModelSQL


class UsersModel(BaseModelSQL):
    __tablename__ = 'users'

    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    roles = relationship('RolesModel', secondary='user_role')
