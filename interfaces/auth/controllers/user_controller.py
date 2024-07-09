from typing import List
import logging

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from application.auth.schemas.user_schema import UserSchema
from application.auth.services.user_service import UserService

from application.auth.adapters.user_service_factory import get_user_service

user_router = APIRouter(prefix='/api/v1', tags=['user'])

logger = logging.getLogger(__name__)


@user_router.get(
    '/users',
    response_model=List[UserSchema]
)
async def get_users(service: UserService = Depends(get_user_service)) -> JSONResponse:
    try:
        users = service.get_all_users()
        return JSONResponse(content=users, status_code=200)
    except Exception as e:
        logger.error(f"Error fetching users: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch users") from e
