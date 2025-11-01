from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.crud.crud_user import create_user, get_user_by_email
from app.core.security import verify_password, create_access_token
from app.db.session import get_db
from app.core.logger import logger

router = APIRouter()

@router.post("/register")
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    logger.info(user_in)
    existing = get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = create_user(db, user_in)
    return {"id": user.id, "email": user.email}

@router.post("/login")
def login(user_in: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(db, user_in.username)
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
