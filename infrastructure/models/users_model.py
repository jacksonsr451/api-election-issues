from uuid import uuid4

from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import relationship

from infrastructure.models.base_model_sql import BaseModelSQL


class UsersModel(BaseModelSQL):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid4)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    roles = relationship('RolesModel', secondary='user_role')
