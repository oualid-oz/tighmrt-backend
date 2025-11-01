from fastapi import APIRouter, Depends
from fastapi.routing import APIRoute
from app.api.v1 import auth, task, task_list, user
from app.deps.auth import get_current_user

routers = APIRouter()

# Public routes
routers.include_router(auth.router, prefix="/auth", tags=["auth"])

# Protected routes with automatic user injection
protected_router = APIRouter(route_class=APIRoute, dependencies=[Depends(get_current_user)])
protected_router.include_router(task.router, prefix="/tasks", tags=["tasks"])
protected_router.include_router(task_list.router, prefix="/lists", tags=["lists"])
protected_router.include_router(user.router, prefix="/users", tags=["users"])

# Include protected routes
routers.include_router(protected_router)