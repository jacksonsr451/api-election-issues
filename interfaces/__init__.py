from fastapi import FastAPI

from interfaces.answers.controllers.answers_controller import answers_router
from interfaces.auth.controllers.token_controller import token_router
from interfaces.auth.controllers.user_controller import user_router
from interfaces.election_issues.controllers.election_issues_controller import (
    election_issues_router,
)


def init_routes(app: FastAPI) -> None:
    app.include_router(user_router)
    app.include_router(token_router)
    app.include_router(election_issues_router)
    app.include_router(answers_router)
