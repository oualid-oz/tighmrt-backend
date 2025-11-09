from typing import List, Optional, Tuple, TypeVar, Type, Any, Dict
from sqlalchemy import or_, and_
from sqlalchemy.orm import Session
import uuid
from datetime import datetime

from app.models.task_list import TaskList
from app.schemas.task_list import TaskListCreate, TaskListSearchCriteria, TaskListResponse
from app.schemas.pagination import PaginationParams

ModelType = TypeVar("ModelType", bound=Any)
CreateSchemaType = TypeVar("CreateSchemaType", bound=Any)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=Any)

def model_to_dict(model: Any) -> Dict[str, Any]:
    """Convert SQLAlchemy model to dictionary."""
    if hasattr(model, '__table__'):
        return {c.name: getattr(model, c.name) for c in model.__table__.columns}
    return {}

def model_to_pydantic(model: Any, pydantic_model: Type[ModelType]) -> ModelType:
    """Convert SQLAlchemy model to Pydantic model."""
    model_dict = model_to_dict(model)
    return pydantic_model(**model_dict)

def create_task_list(db: Session, user_id: int, task_list_in: TaskListCreate) -> TaskListResponse:
    db_list = TaskList(
        id=uuid.uuid4(),
        user_id=user_id,
        **task_list_in.dict(exclude={"user_id"}, exclude_unset=True)
    )
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return model_to_pydantic(db_list, TaskListResponse)

def _apply_search_criteria(query, criteria: TaskListSearchCriteria):
    """Apply search criteria to the query"""
    if criteria.name:
        query = query.filter(TaskList.name.ilike(f'%{criteria.name}%'))
    if criteria.created_after:
        query = query.filter(TaskList.created_at >= criteria.created_after)
    if criteria.created_before:
        query = query.filter(TaskList.created_at <= criteria.created_before)
    
    # Apply ordering
    order_by_field = getattr(TaskList, criteria.order_by, TaskList.created_at)
    if criteria.order == 'desc':
        order_by_field = order_by_field.desc()
    else:
        order_by_field = order_by_field.asc()
    
    return query.order_by(order_by_field)

def get_task_lists(
    db: Session, 
    user_id: int,
    pagination: PaginationParams,
    criteria: Optional[TaskListSearchCriteria] = None
) -> Tuple[List[TaskListResponse], int]:
    """
    Get paginated task lists with optional search criteria.
    Returns a tuple of (items, total_count)
    """
    query = db.query(TaskList).filter(TaskList.user_id == user_id)
    
    if criteria:
        query = _apply_search_criteria(query, criteria)
    
    total = query.count()
    items = query.offset((pagination.page - 1) * pagination.size).limit(pagination.size).all()
    
    # Convert SQLAlchemy models to Pydantic models
    pydantic_items = [model_to_pydantic(item, TaskListResponse) for item in items]
    return pydantic_items, total

def get_task_list_by_id(db: Session, task_list_id: int) -> Optional[TaskListResponse]:
    task_list = db.query(TaskList).filter(TaskList.id == task_list_id).first()
    if not task_list:
        return None
    return model_to_pydantic(task_list, TaskListResponse)

def search_task_lists(
    db: Session, 
    user_id: int, 
    query: str,
    pagination: PaginationParams
) -> Tuple[List[TaskListResponse], int]:
    """
    Search task lists by name or description.
    Returns a tuple of (items, total_count)
    """
    search_query = f'%{query}%'
    base_query = db.query(TaskList).filter(
        TaskList.user_id == user_id,
        or_(
            TaskList.name.ilike(search_query),
            TaskList.description.ilike(search_query) if query else None
        )
    )
    
    total = base_query.count()
    items = base_query.offset(
        (pagination.page - 1) * pagination.size
    ).limit(pagination.size).all()
    
    # Convert SQLAlchemy models to Pydantic models
    pydantic_items = [model_to_pydantic(item, TaskListResponse) for item in items]
    return pydantic_items, total

def update_task_list(db: Session, task_list_id: int, task_list_in: TaskListCreate) -> Optional[TaskListResponse]:
    db_list = db.query(TaskList).filter(TaskList.id == task_list_id).first()
    if not db_list:
        return None
    
    update_data = task_list_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_list, field, value)
    
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return model_to_pydantic(db_list, TaskListResponse)
    
def delete_task_list(db: Session, task_list_id: int) -> Optional[TaskListResponse]:
    db_list = db.query(TaskList).filter(TaskList.id == task_list_id).first()
    if not db_list:
        return None
    
    # Convert to Pydantic model before deletion
    result = model_to_pydantic(db_list, TaskListResponse)
    db.delete(db_list)
    db.commit()
    return result
    