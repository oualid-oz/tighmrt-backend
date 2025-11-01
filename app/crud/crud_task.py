from app.models.task import Task
from app.schemas.task import TaskCreate
from sqlalchemy.orm import Session

def create_task(db: Session, task_list_id: int, task_in: TaskCreate):
    db_task = Task(**task_in.dict(), task_list_id=task_list_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks_by_list(db: Session, task_list_id: int):
    return db.query(Task).filter(Task.task_list == task_list_id).all()

def get_tasks_by_user(db: Session, user_id: int):
    return db.query(Task).filter(Task.user_id == user_id).all()

def update_task(db: Session, task_id: int, task_in: TaskCreate):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        return None
    db_task.title = task_in.title or db_task.title
    db_task.description = task_in.description or db_task.description
    db_task.is_completed = task_in.is_completed or db_task.is_completed
    db_task.due_date = task_in.due_date or db_task.due_date
    db.commit()
    db.refresh(db_task)
    return db_task
    