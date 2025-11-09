from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime

from .pagination import PaginationParams, PaginatedResponse


# ---- Base ----
class TaskListBase(BaseModel):
    name: str
    color: str
    description: Optional[str] = None


# ---- Create ----
class TaskListCreate(TaskListBase):
    user_id: UUID


# ---- Update ----
class TaskListUpdate(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None
    description: Optional[str] = None


# ---- Response ----
class TaskListResponse(TaskListBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    tasks: Optional[List[UUID]] = None


# ---- Search Criteria ----
class TaskListSearchCriteria(BaseModel):
    name: Optional[str] = Field(None, description="Filter by task list name (case-insensitive contains)")
    color: Optional[str] = Field(None, description="Filter by task list color (case-insensitive contains)")
    created_after: Optional[datetime] = Field(None, description="Filter by creation date after")
    created_before: Optional[datetime] = Field(None, description="Filter by creation date before")
    order_by: str = Field("created_at", description="Field to order by")
    order: str = Field("desc", pattern="^(asc|desc)$", description="Sort order: asc or desc")


# ---- Paginated Response ----
class PaginatedTaskListResponse(PaginatedResponse[TaskListResponse]):
    pass  # List of task IDs in this list

    class Config:
        from_attributes = True
