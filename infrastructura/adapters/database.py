from decouple import config

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine(config('DATABASE_URL'))


def get_session() -> Session:
    with Session(engine) as session:
        yield session
