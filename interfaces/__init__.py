from fastapi import FastAPI

from interfaces.auth.controllers.token_controller import token_router
from interfaces.auth.controllers.user_controller import user_router


def init_routes(app: FastAPI) -> None:
    app.include_router(user_router)
    app.include_router(token_router)
