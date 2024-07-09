from fastapi import FastAPI

from interfaces.auth.controllers.user_controller import user_router


def init_routes(app: FastAPI) -> None:
    app.include_router(user_router)
