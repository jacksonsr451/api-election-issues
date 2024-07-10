from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from rich import status

from infrastructure.models.users_model import UsersModel
from infrastructure.repositories.user_repository import UserRepository
from application.auth.adapters.access_token import AccessToken

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/token')


def get_user_repository() -> UserRepository:
    return UserRepository(UsersModel)


def get_current_user(
    user_repository: UserRepository = Depends(get_user_repository),
    token: str = Depends(oauth2_scheme)
):
    claims = AccessToken.verify_token(token=token)
    if user := user_repository.get_by_id(claims['sub']):
        return user
    else:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='User not found',
        )
