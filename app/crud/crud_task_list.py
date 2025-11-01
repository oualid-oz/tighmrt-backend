from app.models.task_list import TaskList
from app.schemas.task_list import TaskListCreate
from sqlalchemy.orm import Session

def create_task_list(db: Session, user_id: int, task_list_in: TaskListCreate):
    db_list = TaskList(name=task_list_in.name, user_id=user_id)
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return db_list

def get_task_lists(db: Session, user_id: int):
    return db.query(TaskList).filter(TaskList.user_id == user_id).all()

def update_task_list(db: Session, task_list_id: int, task_list_in: TaskListCreate):
    db_list = db.query(TaskList).filter(TaskList.id == task_list_id).first()
    if not db_list:
        return None
    db_list.name = task_list_in.name or db_list.name
    db.commit()
    db.refresh(db_list)
    return db_list
    
def delete_task_list(db: Session, task_list_id: int):
    db_list = db.query(TaskList).filter(TaskList.id == task_list_id).first()
    if not db_list:
        return None
    db.delete(db_list)
    db.commit()
    return db_list
    