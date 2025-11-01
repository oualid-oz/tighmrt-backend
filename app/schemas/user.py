from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.schemas.role import RoleResponse

# ---- Base ----
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    username: Optional[str] = None
    active: Optional[bool] = True
    deleted: Optional[bool] = False

# ---- Create ----
class UserCreate(UserBase):
    password: str
    role_id: str

# ---- Update ----
class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None
    active: Optional[bool] = None
    deleted: Optional[bool] = None
    role_id: Optional[UUID] = None

# ---- Response ----
class UserResponse(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    role: Optional[RoleResponse] = None

    class Config:
        from_attributes = True
