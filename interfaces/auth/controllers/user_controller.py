from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from application.auth.schemas.user_schema import UserSchema, UserCreate, UserUpdate
from application.auth.services.user_service import UserService

user_router = APIRouter(prefix='/api/v1/users', tags=['user'])


@user_router.get('/users', response_model=List[UserSchema])
async def get_users(service: UserService = Depends(UserService)) -> JSONResponse:
    try:
        user = service.get_all_users()
        return JSONResponse(content=user, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))