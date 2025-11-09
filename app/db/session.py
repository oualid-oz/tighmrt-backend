from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import Depends
from typing import Annotated
import os

# Example PostgreSQL URL — update with your actual credentials
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL or "postgresql+psycopg2://postgres:postgres@localhost:5432/taskdb")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

DBSession = Annotated[SessionLocal, Depends(get_db)]
