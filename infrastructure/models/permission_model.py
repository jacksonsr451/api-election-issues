from sqlalchemy import Column, String, UUID
from uuid import uuid4

from infrastructure.models.base_model_sql import BaseModelSQL


class PermissionModel(BaseModelSQL):
    __tablename__ = 'permissions'

    name = Column(String(50), unique=True, nullable=False)
