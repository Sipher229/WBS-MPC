from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings


# The engine handles the connection to the DB
engine = create_engine(settings.database_url)

# Each instance of SessionLocal will be a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass
# Dependency to get a DB session for FastAPI routes


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# try:
#     with engine.connect() as connection:
#         print("Connection successful")
#
# except OperationalError as e:
#     print("DB connection failed")
