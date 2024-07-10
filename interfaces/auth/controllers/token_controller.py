import logging

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from http import HTTPStatus

from application.auth.adapters.access_token import AccessToken
from application.auth.services.user_service import UserService
from application.auth.adapters.access_token_factory import get_access_token
from application.auth.adapters.user_service_factory import get_user_service
from application.auth.schemas.token_schema import TokenSchema

token_router = APIRouter(prefix='/api/v1', tags=['Token'])

logger = logging.getLogger(__name__)


@token_router.post(
    '/token',
    summary='Create a token',
    response_model=TokenSchema,
)
async def create_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service),
    token_service: AccessToken = Depends(get_access_token),
):
    try:
        user = user_service.login(form_data.username, form_data.password)
        exp, access_token = token_service.create_access_token(user.id.__str__())

        return JSONResponse(
            content=TokenSchema(
                access_token=access_token,
                token_type='Bearer',
                expires_in=exp
            ).model_dump(), status_code=200
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect username or password',
        ) from e
