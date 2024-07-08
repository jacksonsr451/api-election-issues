from uuid import uuid4

from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import relationship

from infrastructure.models.base_model_sql import BaseModelSQL


class RolesModel(BaseModelSQL):
    __tablename__ = 'roles'
    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid4)
    name = Column(String(50), unique=True)

    users = relationship('UsersModel', secondary='user_role')
