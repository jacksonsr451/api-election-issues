from sqlalchemy import UUID, Column, ForeignKey, Table

from infrastructure.models.base_model_sql import BaseModelSQL

role_user_table = Table(
    'user_role',
    BaseModelSQL.metadata,
    Column(
        'user_id', UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True
    ),
    Column(
        'role_id', UUID(as_uuid=True), ForeignKey('roles.id'), primary_key=True
    ),
)
