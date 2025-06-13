from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from entities.subtask import Subtask
from todos.subtasks.models import SubtaskGet, SubtaskCreate, SubtaskEdit


def get_subtask_by_subtask_id(db : Session, subtask_id : int) -> SubtaskGet:
    db_subtask = db.query(Subtask).filter(Subtask.id_subtask == subtask_id).first()
    if db_subtask is None:
        raise HTTPException(HTTP_404_NOT_FOUND, "Subtask is not found")
    return db_subtask

def get_subtasks_by_task_id(db : Session, task_id : int) -> List[SubtaskGet]:
    db_subtasks = db.query(Subtask).filter(Subtask.id_task == task_id).all()
    return [SubtaskGet(title=subtask.title , is_completed=subtask.is_completed) for subtask in db_subtasks]

def create_subtasks(db: Session, subtasks: List[SubtaskCreate]):
    try:
        db_subtasks =[Subtask( ** subtask.model_dump()) for subtask in subtasks]
        db.add_all(db_subtasks)
        db.commit()
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST ,f"Failed to create subtasks. Error: {str(e)}")
    return subtasks

def edit_subtask(db: Session, subtask_id: int , subtask: SubtaskEdit) -> SubtaskGet:
    if not subtask.model_fields_set:
        raise HTTPException(HTTP_400_BAD_REQUEST, "Subtask Edit Request body was empty")
    db_subtask = db.query(Subtask).filter(Subtask.id_subtask == subtask_id).first()
    if db_subtask is None:
        raise HTTPException(HTTP_404_NOT_FOUND, "Subtask is not found")
    if subtask.title is not None:
        db_subtask.title = subtask.title
    if subtask.is_completed is not None:
        db_subtask.is_completed = subtask.is_completed
    db.commit()
    db.refresh(db_subtask)
    return SubtaskGet(title=db_subtask.title, is_completed=db_subtask.is_completed)

def delete_subtask(db : Session , subtask_id: int):
    db_subtask = db.query(Subtask).filter(Subtask.id_subtask == subtask_id).first()
    if db_subtask is None:
        raise HTTPException(HTTP_404_NOT_FOUND, "No subtask found by given subtask_id")
    db.delete(db_subtask)
    db.commit()

def delete_subtasks_by_task_id(db: Session, task_id: int):
    db.query(Subtask).filter(Subtask.id_task == task_id).delete()
    db.commit()
    return