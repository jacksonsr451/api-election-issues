import logging
from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.testing.pickleable import User

from application.auth.adapters.access_token import AccessToken
from application.auth.adapters.access_token_factory import get_access_token
from application.auth.adapters.current_user import get_current_user
from application.auth.adapters.user_service_factory import get_user_service
from application.auth.adapters.validate import Validate, get_validate
from application.auth.schemas.token_schema import TokenSchema
from application.auth.schemas.user_schema import (
    UpdateUserPassword,
    UserCreate,
    UserLogin,
    UserSchema,
    UserUpdate,
)
from application.auth.services.user_service import UserService

user_router = APIRouter(prefix='/api/v1', tags=['Users'])

logger = logging.getLogger(__name__)


@user_router.get(
    '/users',
    summary='Get all users',
    response_model=List[UserSchema],
)
async def get_users(
    service: UserService = Depends(get_user_service),
    current_user=Depends(get_current_user),
    validate: Validate = Depends(get_validate),
) -> JSONResponse:
    try:
        user, _token = current_user
        validate.validate_role(user, ['admin', 'editor'])

        users = service.get_all_users()
        return JSONResponse(content=users, status_code=200)
    except Exception as e:
        logger.error(f'Error fetching users: {str(e)}')
        error_message = str(e).split('\n')[0]
        status_code = (
            e.status_code
            if hasattr(e, 'status_code')
            else HTTPStatus.INTERNAL_SERVER_ERROR
        )
        return JSONResponse(
            content={'error': error_message}, status_code=status_code
        )


@user_router.get(
    '/users/{user_id}',
    summary='Get a specific user',
    response_model=UserSchema,
)
async def get_user(
    user_id: str,
    service: UserService = Depends(get_user_service),
    current_user=Depends(get_current_user),
    validate: Validate = Depends(get_validate),
) -> JSONResponse:
    try:
        user, _token = current_user
        if user.id.__str__() != user_id:
            validate.validate_role(user, ['admin'])

        user = service.get_user(user_id)
        return JSONResponse(content=user, status_code=200)
    except Exception as e:
        logger.error(f'Error fetching user: {str(e)}')
        error_message = str(e).split('\n')[0]
        status_code = (
            e.status_code
            if hasattr(e, 'status_code')
            else HTTPStatus.INTERNAL_SERVER_ERROR
        )
        return JSONResponse(
            content={'error': error_message}, status_code=status_code
        )


@user_router.post(
    '/users',
    summary='Create a new user',
    response_model=UserSchema,
)
async def create_user(
    data: UserCreate, service: UserService = Depends(get_user_service)
) -> JSONResponse:
    try:
        user = service.create_user(data)
        return JSONResponse(content=user, status_code=200)
    except Exception as e:
        logger.error(f'Error creating user: {str(e)}')
        error_message = str(e).split('\n')[0]
        status_code = (
            e.status_code
            if hasattr(e, 'status_code')
            else HTTPStatus.INTERNAL_SERVER_ERROR
        )
        return JSONResponse(
            content={'error': error_message}, status_code=status_code
        )


@user_router.put(
    '/users/{user_id}',
    summary='Update a user',
    response_model=UserSchema,
)
async def update_user(
    user_id: str,
    data: UserUpdate,
    service: UserService = Depends(get_user_service),
    current_user=Depends(get_current_user),
    validate: Validate = Depends(get_validate),
) -> JSONResponse:
    try:
        user, _token = current_user

        if user.id.__str__() != user_id:
            validate.validate_role(user, ['admin'])

        user = await service.update_user(user_id, data)
        return JSONResponse(content=user, status_code=200)
    except Exception as e:
        logger.error(f'Error updating user: {str(e)}')
        error_message = str(e).split('\n')[0]
        status_code = (
            e.status_code
            if hasattr(e, 'status_code')
            else HTTPStatus.INTERNAL_SERVER_ERROR
        )
        return JSONResponse(
            content={'error': error_message}, status_code=status_code
        )


@user_router.put(
    '/users/{user_id}/password',
    summary='Update password of a user',
    response_model=UserSchema,
)
async def update_user_password(
    user_id: str,
    data: UpdateUserPassword,
    service: UserService = Depends(get_user_service),
    current_user=Depends(get_current_user),
) -> JSONResponse:
    try:
        user, _token = current_user

        if user.id.__str__() != user_id:
            raise HTTPException(
                status_code=403,
                detail='User request permission denied',
            )

        user = service.update_password(user_id, data)
        return JSONResponse(content=user, status_code=200)
    except Exception as e:
        logger.error(f'Error updating user: {str(e)}')
        error_message = str(e).split('\n')[0]
        status_code = (
            e.status_code
            if hasattr(e, 'status_code')
            else HTTPStatus.INTERNAL_SERVER_ERROR
        )
        return JSONResponse(
            content={'error': error_message}, status_code=status_code
        )


@user_router.put(
    '/users/{user_id}/roles/{role_name}',
    summary='Update role a user',
    response_model=UserSchema,
)
async def update_user_roles(
    user_id: str,
    role_name: str,
    service: UserService = Depends(get_user_service),
    current_user=Depends(get_current_user),
    validate: Validate = Depends(get_validate),
) -> JSONResponse:
    try:
        user, _token = current_user
        validate.validate_role(user, ['admin'])

        user = service.update_user_role(user_id, role_name)
        return JSONResponse(content=user, status_code=200)
    except Exception as e:
        logger.error(f'Error updating user: {str(e)}')
        error_message = str(e).split('\n')[0]
        status_code = (
            e.status_code
            if hasattr(e, 'status_code')
            else HTTPStatus.INTERNAL_SERVER_ERROR
        )
        return JSONResponse(
            content={'error': error_message}, status_code=status_code
        )


@user_router.delete(
    '/users/{user_id}',
    summary='Delete a user',
)
async def delete_user(
    user_id: str,
    service: UserService = Depends(get_user_service),
    current_user=Depends(get_current_user),
    validate: Validate = Depends(get_validate),
) -> JSONResponse:
    try:
        user, _token = current_user
        validate.validate_role(user, ['admin'])

        service.delete_user(user_id)
        return JSONResponse(
            content={'message': 'User has been deleted!'}, status_code=200
        )
    except Exception as e:
        logger.error(f'Error deleting user: {str(e)}')
        error_message = str(e).split('\n')[0]
        status_code = (
            e.status_code
            if hasattr(e, 'status_code')
            else HTTPStatus.INTERNAL_SERVER_ERROR
        )
        return JSONResponse(
            content={'error': error_message}, status_code=status_code
        )


@user_router.post(
    '/login',
    summary='Login a user',
    response_model=TokenSchema,
)
def login(
    data: UserLogin,
    user_service: UserService = Depends(get_user_service),
    token_service: AccessToken = Depends(get_access_token),
) -> JSONResponse:
    try:
        user = user_service.login(**data.model_dump())
        exp, access_token = token_service.create_access_token(
            user.id.__str__()
        )
        response = TokenSchema(
            access_token=access_token, token_type='Bearer', expires_in=exp
        ).model_dump()
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        logger.error(f'Error logging in: {str(e)}')
        error_message = str(e).split('\n')[0]
        status_code = (
            e.status_code
            if hasattr(e, 'status_code')
            else HTTPStatus.INTERNAL_SERVER_ERROR
        )
        return JSONResponse(
            content={'error': error_message}, status_code=status_code
        )


@user_router.get(
    '/logout',
    summary='Logout a user',
)
def logout(
    current_user: User = Depends(get_current_user),
    token_services: AccessToken = Depends(get_access_token),
) -> JSONResponse:
    _user, token = current_user
    token_services.invalidate_token(token)

    response = JSONResponse(
        content={'message': 'User has been logged out!'}, status_code=200
    )
    response.delete_cookie(key='Authorization')
    return response
