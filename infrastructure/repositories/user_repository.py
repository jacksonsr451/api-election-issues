from typing import Optional

from sqlalchemy.orm import joinedload

from domain.auth.user_entity import UserEntity
from domain.auth.services.password_encryption_service import (
    PasswordEncryptionService,
)
from infrastructure.exceptions.database_exception import DatabaseException
from infrastructure.models import RolesModel, UsersModel, BaseModelSQL
from infrastructure.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, model: UsersModel):
        BaseRepository.__init__(self, model=model)

    def create(self, data: UserEntity) -> Optional[UsersModel]:
        try:
            data = data.model_dump()
            roles = data.get('roles', [])
            if not roles:
                guest_role = (
                    self.db.query(RolesModel).filter_by(name='guest').first()
                )
                if guest_role is None:
                    raise DatabaseException(
                        message='Role "guest" not found', status_code=404
                    )
                roles = [guest_role]
            else:
                role = (
                    self.db.query(RolesModel)
                    .filter_by(RolesModel.id in roles)
                    .first()
                )
                if role is None:
                    raise DatabaseException(
                        message='Role id not found', status_code=404
                    )
                roles.append(role)

<<<<<<< HEAD
            data['password'] = PasswordEncryptionService.encrypt_password('admin')
=======
            if 'password' not in data:
                data['password'] = PasswordEncryptionService.encrypt_password('admin')

>>>>>>> 7eadb9b713e6a4e07dc281ea823216badde4c76e
            create_data = UsersModel.from_model(**data)
            create_data.roles = roles

            self.db.add(create_data)
            return self._extracted_from_update_5(create_data)
        except Exception as e:
            name = UsersModel.__name__.replace('Model', '')
            raise DatabaseException(
                message=f'{name} with id {id} not found', status_code=404
            ) from e

    def get_all(self) -> list:
        return (
            self.db.query(UsersModel)
            .options(
                joinedload(UsersModel.roles).joinedload(RolesModel.permissions)
            )
            .all()
        )

    def update(self, id: str, data: UserEntity) -> BaseModelSQL | None:
        try:
            instance_user = self.db.query(UsersModel).filter_by(id=id).first()

            if not instance_user:
                raise ValueError('Instance not found')

            data_dict = data.model_dump()

            if 'password' not in data_dict:
                data_dict['password'] = PasswordEncryptionService.encrypt_password('admin')

            data_roles = data_dict.get('roles', [])
            del data_dict['roles']

            for key, value in data_dict.items():
                if hasattr(instance_user, key) and value is not None:
                    if (
                        key != 'id'
                        and key in UsersModel.__table__.columns.keys()
                    ):
                        setattr(instance_user, key, value)

            def has_role(user, role_id):
                for role in user.roles:
                    if role.id == role_id:
                        return True
                return False

            for data_role in data_roles:
                name = data_role.get('name')

                if name:
                    role_instance = (
                        self.db.query(RolesModel)
                        .filter_by(name=name)
                        .first()
                    )

                    if not has_role(instance_user, role_instance.id):
                        instance_user.roles.append(role_instance)
            self.db.add(instance_user)
            return self._extracted_from_update_5(instance_user)

        except Exception as e:
            print(f'Erro ao atualizar registro: {str(e)}')
            self.db.rollback()
            raise e

    def update_user_role(self, user_id: str, role_name: str) -> UsersModel:
        if user := self.db.query(UsersModel).filter_by(id=user_id).first():
            role = self.get_role(role_name)
            if not role:
                raise DatabaseException(
                    message=f'Role "{role_name}" not found', status_code=404
                )
            user.roles.append(role)
            self.db.add(user)
            return self._extracted_from_update_5(user)
        else:
            raise DatabaseException(
                message='User does not exist', status_code=404
            )

    def get_role(self, name: str) -> Optional[RolesModel]:
        return self.db.query(RolesModel).filter_by(name=name).first()

    def get_user_by_email(self, email: str):
        try:
            return (
                self.db.query(UsersModel)
                .filter(UsersModel.email == email)
                .first()
            )
        except Exception as e:
            name = UsersModel.__name__.replace('Model', '')
            raise DatabaseException(
                message=f'{e} with email: {email} not found', status_code=404
            ) from e

