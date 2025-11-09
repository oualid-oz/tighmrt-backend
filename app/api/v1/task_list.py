from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Request, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import crud_task_list
from app.schemas.task_list import (
    TaskListCreate, 
    TaskListUpdate,
    TaskListSearchCriteria,
    PaginatedTaskListResponse,
    TaskListResponse
)
from app.schemas.pagination import PaginationParams

router = APIRouter()

@router.post("/", response_model=TaskListResponse, status_code=status.HTTP_201_CREATED)
async def create_task_list(
    request: Request, 
    task_list_in: TaskListCreate, 
    db: Session = Depends(get_db)
):
    """
    Create a new task list.
    """
    return crud_task_list.create_task_list(db, request.state.current_user.id, task_list_in)

@router.get("/", response_model=PaginatedTaskListResponse)
async def get_lists(
    request: Request,
    page: int = Query(1, ge=1, description="Page number starting from 1"),
    size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    name: str = Query(None, description="Filter by task list name"),
    created_after: str = Query(None, description="Filter by creation date after (ISO 8601 format)"),
    created_before: str = Query(None, description="Filter by creation date before (ISO 8601 format)"),
    order_by: str = Query("created_at", description="Field to order by"),
    order: str = Query("desc", description="Sort order: 'asc' or 'desc'"),
    db: Session = Depends(get_db)
):
    """
    Get paginated list of task lists with optional filtering and sorting.
    """
    pagination = PaginationParams(page=page, size=size)
    
    # Build search criteria
    criteria = TaskListSearchCriteria(
        name=name,
        created_after=created_after,
        created_before=created_before,
        order_by=order_by,
        order=order
    )
    
    # Get paginated results
    items, total = crud_task_list.get_task_lists(
        db=db,
        user_id=request.state.current_user.id,
        pagination=pagination,
        criteria=criteria
    )
    
    return PaginatedTaskListResponse.create(
        items=items,
        total=total,
        pagination=pagination
    )

@router.get("/search", response_model=PaginatedTaskListResponse)
async def search_lists(
    request: Request,
    query: str,
    page: int = Query(1, ge=1, description="Page number starting from 1"),
    size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    db: Session = Depends(get_db)
):
    """
    Search task lists by name or description with pagination.
    """
    pagination = PaginationParams(page=page, size=size)
    
    data, total = crud_task_list.search_task_lists(
        db=db,
        user_id=request.state.current_user.id,
        query=query,
        pagination=pagination
    )
    
    return PaginatedTaskListResponse.create(
        data=data,
        total=total,
        pagination=pagination
    )

@router.get("/{task_list_id}", response_model=TaskListResponse)
async def get_task_list(
    request: Request, 
    task_list_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a specific task list by ID.
    """
    task_list = crud_task_list.get_task_list_by_id(db, task_list_id)
    if not task_list or str(task_list.user_id) != str(request.state.current_user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task list not found"
        )
    return task_list

@router.put("/{task_list_id}", response_model=TaskListResponse)
async def update_task_list(
    request: Request, 
    task_list_id: str,
    task_list_in: TaskListUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a task list.
    """
    # First get the task list to check ownership
    existing = crud_task_list.get_task_list(db, task_list_id)
    if not existing or str(existing.user_id) != str(request.state.current_user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task list not found"
        )
    
    updated_task_list = crud_task_list.update_task_list(
        db=db,
        task_list_id=task_list_id,
        task_list_in=task_list_in
    )
    
    if not updated_task_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task list not found"
        )
    
    return updated_task_list

@router.delete("/{task_list_id}", response_model=TaskListResponse)
async def delete_task_list(
    request: Request,
    task_list_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a task list.
    """
    # First get the task list to check ownership
    existing = crud_task_list.get_task_list(db, task_list_id)
    if not existing or str(existing.user_id) != str(request.state.current_user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task list not found"
        )
    
    deleted_task_list = crud_task_list.delete_task_list(db, task_list_id)
    if not deleted_task_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task list not found"
        )
    
    return deleted_task_list
