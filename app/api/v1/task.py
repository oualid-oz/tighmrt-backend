from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import crud_task

router = APIRouter()

@router.post("/")
def create_task():
    pass

@router.get("/")
def get_tasks(request: Request, db: Session = Depends(get_db)):
    return crud_task.get_tasks_by_user(db, request.state.current_user.id)

@router.get("/{task_id}")
def get_task(request: Request, task_id: int):
    pass

@router.put("/{task_id}")
def update_task(request: Request, task_id: int):
    pass

@router.delete("/{task_id}")
def delete_task(request: Request, task_id: int):
    pass