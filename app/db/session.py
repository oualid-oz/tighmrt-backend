from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import Depends
from typing import Annotated
from app.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DBSession = Annotated[SessionLocal, Depends(get_db)]
