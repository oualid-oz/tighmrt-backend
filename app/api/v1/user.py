from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserCreate
from app.deps.common import common_pagination
from app.crud import crud_user

router = APIRouter()


@router.post("/")
def create_user(request: Request, user_in: UserCreate, db: Session = Depends(get_db)):
    return crud_user.create_user(db, user_in)


@router.get("/")
def get_users(
    request: Request,
    db: Session = Depends(get_db),
    pagination: dict = Depends(common_pagination),
):
    current_user = request.state.current_user
    return crud_user.get_users(current_user, db, pagination)


@router.get("/{user_id}")
def get_user(request: Request, user_id: str, db: Session = Depends(get_db)):
    current_user = request.state.current_user
    return crud_user.get_user(user_id, db, current_user)


@router.put("/{user_id}")
def update_user(
    request: Request, user_id: str, user_in: UserCreate, db: Session = Depends(get_db)
):
    current_user = request.state.current_user
    return crud_user.update_user(user_id, user_in, db, current_user)


@router.delete("/{user_id}")
def delete_user(request: Request, user_id: str, db: Session = Depends(get_db)):
    current_user = request.state.current_user
    return crud_user.delete_user(user_id, db, current_user)
