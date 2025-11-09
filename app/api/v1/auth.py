from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.user import UserResponse
from app.crud.crud_user import get_user_by_email
from app.core.security import verify_password, create_access_token, get_current_user
from app.db.session import get_db

router = APIRouter()

@router.post("/login")
def login(user_in: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(db, user_in.username)
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
async def read_users_me(current_user: UserResponse = Depends(get_current_user)):
    return current_user
