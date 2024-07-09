from sqlalchemy.orm import configure_mappers

from infrastructure.models.base_model_sql import BaseModelSQL
from infrastructure.models.permission_model import PermissionModel
from infrastructure.models.roles_model import RolesModel
from infrastructure.models.users_model import UsersModel

configure_mappers()

