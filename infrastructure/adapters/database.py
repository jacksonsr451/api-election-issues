from decouple import config

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(config('DATABASE_URL'))

Base = declarative_base()


def get_session() -> Session:
    with Session(engine) as session:
        yield session
