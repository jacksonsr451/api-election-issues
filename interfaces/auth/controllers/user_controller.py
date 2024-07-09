from typing import List
import logging

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from application.auth.schemas.user_schema import UserSchema, UserCreate, UserUpdate, UpdateUserPassword
from application.auth.services.user_service import UserService

from application.auth.adapters.user_service_factory import get_user_service

user_router = APIRouter(prefix='/api/v1', tags=['Users'])

logger = logging.getLogger(__name__)


@user_router.get(
    '/users',
    summary='Get all users',
    response_model=List[UserSchema],
)
async def get_users(service: UserService = Depends(get_user_service)) -> JSONResponse:
    try:
        users = service.get_all_users()
        return JSONResponse(content=users, status_code=200)
    except Exception as e:
        logger.error(f"Error fetching users: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch users") from e


@user_router.get(
    '/users/{user_id}',
    summary='Get a specific user',
    response_model=UserSchema,
)
async def get_user(user_id: str, service: UserService = Depends(get_user_service)) -> JSONResponse:
    try:
        user = service.get_user(user_id)
        return JSONResponse(content=user, status_code=200)
    except Exception as e:
        logger.error(f"Error fetching user: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch user") from e


@user_router.post(
    '/users',
    summary='Create a new user',
    response_model=UserSchema,
)
async def create_user(data: UserCreate, service: UserService = Depends(get_user_service)) -> JSONResponse:
    try:
        user = await service.create_user(data)
        return JSONResponse(content=user, status_code=200)
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create user") from e


@user_router.put(
    '/users/{user_id}',
    summary='Update a user',
    response_model=UserSchema,
)
async def update_user(user_id: str, data: UserUpdate, service: UserService = Depends(get_user_service)) -> JSONResponse:
    try:
        user = await service.update_user(user_id, data)
        return JSONResponse(content=user, status_code=200)
    except Exception as e:
        logger.error(f"Error updating user: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update user") from e


@user_router.put(
    '/users/{user_id}',
    summary='Update password of a user',
    response_model=UserSchema,
)
async def update_user_password(user_id: str, data: UpdateUserPassword, service: UserService = Depends(get_user_service)) -> JSONResponse:
    try:
        user = service.update_password(user_id, data)
        return JSONResponse(content=user, status_code=200)
    except Exception as e:
        logger.error(f"Error updating user: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update user") from e


@user_router.delete(
    '/users/{user_id}',
    summary='Delete a user',
)
async def delete_user(user_id: str, service: UserService = Depends(get_user_service)) -> JSONResponse:
    try:
        service.delete_user(user_id)
        return JSONResponse(content={'message': 'User has been deleted!'}, status_code=200)
    except Exception as e:
        logger.error(f"Error deleting user: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete user") from e
