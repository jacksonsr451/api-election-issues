import logging
from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from application.auth.adapters.current_user import get_current_user
from application.auth.adapters.validate import Validate, get_validate
from application.election_issues.adapters.election_issues_service import (
    get_election_issues_service,
)
from application.election_issues.schemas.election_issues_schemas import (
    ElectionIssues,
    ElectionIssuesCreate,
    ElectionIssuesUpdate,
)
from application.election_issues.services.election_issues_service import (
    ElectionIssuesService,
)

election_issues_router = APIRouter(prefix='/api/v1', tags=['Election Issues'])

logger = logging.getLogger(__name__)


@election_issues_router.get(
    '/election-issues',
    summary='Get all election issues',
    response_model=List[ElectionIssues],
)
async def list_election_issues(
    service: ElectionIssuesService = Depends(get_election_issues_service),
    current_user=Depends(get_current_user),
    validate: Validate = Depends(get_validate),
) -> JSONResponse:
    try:
        user, _token = current_user
        validate.validate_role(user, ['admin', 'publisher'])

        response = service.get_all_election_issues()
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


@election_issues_router.get(
    '/election-issues/{issue_id}',
    summary='Get election issues by id',
    response_model=ElectionIssues,
)
def get_election_issue(
    issue_id: str,
    service: ElectionIssuesService = Depends(get_election_issues_service),
    current_user=Depends(get_current_user),
    validate: Validate = Depends(get_validate),
) -> JSONResponse:
    try:
        user, _token = current_user
        validate.validate_role(user, ['admin', 'publisher'])

        response = service.get_election_issue(issue_id)
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


@election_issues_router.post(
    '/election-issues',
    summary='Create a election issues',
    response_model=ElectionIssues,
)
def create_election_issue(
    data: ElectionIssuesCreate,
    service: ElectionIssuesService = Depends(get_election_issues_service),
    current_user=Depends(get_current_user),
    validate: Validate = Depends(get_validate),
) -> JSONResponse:
    try:
        user, _token = current_user
        validate.validate_role(user, ['admin', 'publisher'])

        response = service.create_election_issue(data)
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


@election_issues_router.put(
    '/election-issues/{issue_id}',
    summary='Update a election issues',
    response_model=ElectionIssues,
)
def update_election_issue(
    issue_id: str,
    data: ElectionIssuesUpdate,
    service: ElectionIssuesService = Depends(get_election_issues_service),
    current_user=Depends(get_current_user),
    validate: Validate = Depends(get_validate),
) -> JSONResponse:
    try:
        user, _token = current_user
        validate.validate_role(user, ['admin', 'publisher'])

        response = service.update_election_issue(issue_id, data)
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


@election_issues_router.delete(
    '/election-issues/{issue_id}',
    summary='Delete a election issues',
    response_model=ElectionIssues,
)
def delete_election_issue(
    issue_id: str,
    service: ElectionIssuesService = Depends(get_election_issues_service),
    current_user=Depends(get_current_user),
    validate: Validate = Depends(get_validate),
) -> JSONResponse:
    try:
        user, _token = current_user
        validate.validate_role(user, ['admin', 'publisher'])

        service.delete_election_issue(issue_id)
        return JSONResponse(
            content={'message': 'Election issue is successfully deleted'},
            status_code=200,
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
