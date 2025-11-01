from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID


# ---- Base ----
class PermissionBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None


# ---- Create ----
class PermissionCreate(PermissionBase):
    pass


# ---- Update ----
class PermissionUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None


# ---- Response ----
class PermissionResponse(PermissionBase):
    id: UUID
    roles: Optional[List[UUID]] = None  # List of role IDs that have this permission

    class Config:
        from_attributes = True
