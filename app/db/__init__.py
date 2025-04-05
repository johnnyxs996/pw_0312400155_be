from typing import Annotated

from fastapi import Depends
from sqlmodel import create_engine, Session, SQLModel

import app.db.models
from app.core.config import settings


DB_CONNECTION_STRING = "postgresql://{}:{}@{}:{}/{}".format(
    settings.DB_USER, settings.DB_PASSWORD,
    settings.DB_HOST, settings.DB_PORT, settings.DB_NAME)

engine = create_engine(DB_CONNECTION_STRING)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
