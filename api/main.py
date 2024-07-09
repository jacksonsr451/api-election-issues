from fastapi import FastAPI

from interfaces import init_routes

app = FastAPI()

init_routes(app=app)
