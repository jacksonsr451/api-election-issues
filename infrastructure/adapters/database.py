from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = config('DATABASE_URL')

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=20,
    max_overflow=40,
    pool_timeout=30,
    pool_recycle=1800,pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
