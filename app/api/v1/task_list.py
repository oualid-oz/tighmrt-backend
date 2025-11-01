from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import crud_task_list
from app.schemas.task_list import TaskListCreate

router = APIRouter()

@router.post("/")
def create_task_list(request: Request, task_list_in: TaskListCreate, db: Session = Depends(get_db)):
    return crud_task_list.create_task_list(db, request.state.current_user.id, task_list_in)

@router.get("/")
def get_lists(request: Request, db: Session = Depends(get_db)):
    return crud_task_list.get_task_lists(db, request.state.current_user.id)

@router.get("/{task_list_id}")
def get_task_list(request: Request, task_list_id: int):
    pass

@router.put("/{task_list_id}")
def update_task_list(request: Request, task_list_id: int):
    pass

@router.delete("/{task_list_id}")
def delete_task_list(task_list_id: int):
    pass
