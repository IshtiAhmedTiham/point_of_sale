import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from fastapi import Depends
from typing import Annotated


POSTGRESQL_DATABASE = os.getenv("POSTGRESQL_DATABASE_URL","")

def get_engine():
    engine = create_engine(POSTGRESQL_DATABASE)
    return engine


Base = declarative_base()


session_local = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
def get_db():
    db = session_local()

    try:
        yield db
    finally:
        db.close()


DbSession = Annotated[Session, Depends(get_db)]

def init_db():
    Base.metadata.create_all(bind=get_engine())
