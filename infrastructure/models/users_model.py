from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from application.auth.schemas.user_schema import UserSchema, PermissionSchema, RoleSchema
from infrastructure.models.base_model_sql import BaseModelSQL
from infrastructure.models.user_role_model import role_user_table


class UsersModel(BaseModelSQL):
    __tablename__ = 'users'

    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    roles = relationship("RolesModel", secondary=role_user_table, back_populates="users")

    def to_schema(self, schema: UserSchema) -> UserSchema:
        user_dict = self.to_dict()
        user_schema = UserSchema(**user_dict)

        role_schemas = []
        for role in self.roles:
            permission_schemas = []
            for permission in role.permissions:
                permission_dict = permission.to_dict()
                permission_schema = PermissionSchema(**permission_dict)
                permission_schemas.append(permission_schema)

            role_dict = role.to_dict()
            role_dict['permissions'] = permission_schemas
            role_schema = RoleSchema(**role_dict)
            role_schemas.append(role_schema)

        user_schema.roles = role_schemas

        return user_schema
