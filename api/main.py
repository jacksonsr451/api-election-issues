from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from interfaces import init_routes

app = FastAPI()

origins = [
    'http://localhost',
    'http://localhost:3000',
    'http://localhost:8080',
<<<<<<< HEAD
    'http://195.200.1.150:8080',
=======
    'http://195.200.1.150:8080'
>>>>>>> 7eadb9b713e6a4e07dc281ea823216badde4c76e
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

init_routes(app=app)
