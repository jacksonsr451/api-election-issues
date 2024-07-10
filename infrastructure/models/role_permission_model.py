from sqlalchemy import UUID, Column, ForeignKey, Table

from infrastructure.models.base_model_sql import BaseModelSQL

role_permission_table = Table(
    'role_permission',
    BaseModelSQL.metadata,
    Column(
        'role_id', UUID(as_uuid=True), ForeignKey('roles.id'), primary_key=True
    ),
    Column(
        'permission_id',
        UUID(as_uuid=True),
        ForeignKey('permissions.id'),
        primary_key=True,
    ),
)
