from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from interfaces import init_routes

app = FastAPI()

origins = [
    'http://localhost',
    'http://localhost:3000',
    'http://localhost:8080',
    'http://195.200.1.150:8080',
    'https://dataprevia.com.br',
    'http://api-election-issues',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

init_routes(app=app)
