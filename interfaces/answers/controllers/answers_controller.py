import logging
from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from application.answers.adapters.answers_service_factory import (
    get_answers_service,
)
from application.answers.schemas.answers_schema import (
    AnswersCreate,
    AnswersSchema,
)
from application.answers.services.answers_service import AnswersService
from application.auth.adapters.current_user import get_current_user
from application.auth.adapters.validate import Validate, get_validate

answers_router = APIRouter(prefix='/api/v1', tags=['Answers'])

logger = logging.getLogger(__name__)


@answers_router.get(
    '/answers/issues/{issue_id}',
    summary='Get all answers',
    response_model=List[AnswersSchema],
)
async def get_all_answers_from_issue(
    issues_id: str,
    service: AnswersService = Depends(get_answers_service),
    current_user=Depends(get_current_user),
    validate: Validate = Depends(get_validate),
) -> JSONResponse:
    try:
        user, _token = current_user
        validate.validate_role(user, ['admin', 'publisher'])

        response = service.get_all_answers(issues_id)
        return JSONResponse(content=response, status_code=200)
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


@answers_router.get(
    '/answers/{id}',
    summary='Get answers',
    response_model=AnswersSchema,
)
async def get_answers(
    id: str,
    service: AnswersService = Depends(get_answers_service),
    current_user=Depends(get_current_user),
    validate: Validate = Depends(get_validate),
) -> JSONResponse:
    try:
        user, _token = current_user
        validate.validate_role(user, ['user', 'admin', 'publisher'])

        response = service.get_answer(id)
        return JSONResponse(content=response, status_code=200)
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


@answers_router.post(
    '/answers',
    summary='Create a new answers',
    response_model=AnswersSchema,
)
async def create_answers(
    data: AnswersCreate,
    service: AnswersService = Depends(get_answers_service),
    current_user=Depends(get_current_user),
    validate: Validate = Depends(get_validate),
) -> JSONResponse:
    try:
        user, _token = current_user
        validate.validate_role(user, ['admin', 'publisher'])

        response = service.include_answer(data)
        return JSONResponse(content=response, status_code=200)
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


@answers_router.delete(
    '/answers/{id}',
    summary='Create a new answers',
    response_model=AnswersSchema,
)
async def delete_answers(
    id: str,
    service: AnswersService = Depends(get_answers_service),
    current_user=Depends(get_current_user),
    validate: Validate = Depends(get_validate),
) -> JSONResponse:
    try:
        user, _token = current_user
        validate.validate_role(user, ['admin', 'publisher'])

        service.delete(id)
        return JSONResponse(
            content={'message': 'Answer deleted successfully'}, status_code=200
        )
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
