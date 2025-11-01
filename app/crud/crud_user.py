from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash
from app.models.role import Role
from sqlalchemy.orm import Session
from uuid import uuid4
from app.core.logger import logger

def create_user(db: Session, user_in: UserCreate):
    role = db.query(Role).filter(Role.code == user_in.role_id).first()
    db_user = User(
        id=uuid4(),
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        phone=user_in.phone,
        email=user_in.email,
        username=user_in.username,
        hashed_password=get_password_hash(user_in.password),
        role_id=role.id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_users(current_user: User, db: Session, pagination: dict) -> list[User]:
    skip = pagination.get("skip", 0)
    limit = pagination.get("limit", 10)
    logger.info(f"Trying to get users with skip: {skip} and limit: {limit} by {current_user.username}")
    return db.query(User).offset(skip).limit(limit).all()

def get_user(user_id: str, db: Session, current_user: User) -> User | None:
    logger.info(f"Trying to get user with id: {user_id} by {current_user.username}")
    return db.query(User).filter(User.id == user_id).first()

def update_user(current_user: User, db: Session, user_id: str, user_in: UserUpdate) -> User | None:
    logger.info(f"Trying to update user with id: {user_id} by {current_user.username}")
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    db_user.email = user_in.email or db_user.email
    db_user.hashed_password = get_password_hash(user_in.password) or db_user.hashed_password
    db_user.first_name = user_in.first_name or db_user.first_name
    db_user.last_name = user_in.last_name or db_user.last_name
    db_user.phone = user_in.phone or db_user.phone
    db_user.username = user_in.username or db_user.username
    db_user.active = user_in.active or db_user.active
    db_user.deleted = user_in.deleted or db_user.deleted
    db.commit()
    db.refresh(db_user)
    logger.info(f"User with id: {user_id} updated by {current_user.username}")
    return db_user
    
def delete_user(db: Session, user_id: str) -> User | None:
    logger.info(f"Trying to delete user with id: {user_id}")
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    logger.info(f"User with id: {user_id} deleted")
    return db_user