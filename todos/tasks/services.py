from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from entities.task import Task
from entities.subtask import Subtask
from entities.priority import Priority
from todos.subtasks import services as subtask_services
from todos.subtasks.models import NewSubtaskGet
from todos.tasks.models import NewTaskCreate, NewTaskGet, NewSubtaskEdit


def get_task_by_task_id(db : Session, task_id : int) -> NewTaskGet:
    db_task = db.query(
        Task.title.label('task_title'),
        Task.is_completed,
        Priority.title.label('priority_title')
    ).filter(
        Task.id_task == task_id
    ).join(
        Priority, Task.id_priority == Priority.id_priority
    ).first()
    if db_task is None:
        raise HTTPException(HTTP_404_NOT_FOUND, "Task is not found")
    db_subtask = subtask_services.get_subtasks_by_task_id(db , task_id)
    return NewTaskGet(subtasks=db_subtask, title=db_task.task_title, priority=db_task.priority_title, is_completed=db_task.is_completed)

def create_task(db: Session , task: NewTaskCreate) -> NewTaskCreate:
    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    return task

def get_tasks_by_list_id(db: Session, list_id : int) -> List[NewTaskGet]:
    db_tasks = db.query(
        Task.title.label('task_title'),
        Task.is_completed.label('task_is_completed'),
        Priority.title.label('priority_title'),
        Subtask.title.label('subtask_title'),
        Subtask.is_completed.label('subtask_is_completed')
    ).select_from(
        Subtask.__table__.outerjoin(Task.__table__, Task.id_task == Subtask.id_task)
    ).join(
        Priority, Task.id_priority == Priority.id_priority
    ).filter(
        Task.id_list == list_id
    ).all()

    tasks = {}
    for (task_title, task_is_completed, priority_title, subtask_title, subtask_is_completed) in db_tasks:
        if task_title not in tasks:
            tasks[task_title] = NewTaskGet(
                title=task_title,
                is_completed=task_is_completed,
                priority=priority_title,
                subtasks=[]
            )
        tasks[task_title].subtasks.append(NewSubtaskGet(title=subtask_title,is_completed=subtask_is_completed))
    return list(tasks.values())