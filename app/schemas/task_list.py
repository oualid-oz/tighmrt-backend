from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime


# ---- Base ----
class TaskListBase(BaseModel):
    name: str
    description: Optional[str] = None


# ---- Create ----
class TaskListCreate(TaskListBase):
    user_id: UUID


# ---- Update ----
class TaskListUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


# ---- Response ----
class TaskListResponse(TaskListBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    tasks: Optional[List[UUID]] = None  # List of task IDs in this list

    class Config:
        from_attributes = True
