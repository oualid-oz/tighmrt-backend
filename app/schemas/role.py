from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID


# ---- Base ----
class RoleBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None


# ---- Create ----
class RoleCreate(RoleBase):
    pass


# ---- Update ----
class RoleUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None


# ---- Response ----
class RoleResponse(RoleBase):
    id: UUID
    users: Optional[List[UUID]] = None  # List of user IDs (optional)
    permissions: Optional[List[UUID]] = None  # List of permission IDs (optional)

    class Config:
        from_attributes = True
