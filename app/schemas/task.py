from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime


# ---- Base ----
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_completed: Optional[bool] = False
    due_date: Optional[datetime] = None


# ---- Create ----
class TaskCreate(TaskBase):
    user_id: UUID
    list_id: UUID


# ---- Update ----
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    due_date: Optional[datetime] = None


# ---- Response ----
class TaskResponse(TaskBase):
    id: UUID
    user_id: UUID
    list_id: UUID
    due_date: datetime

    class Config:
        from_attributes = True
