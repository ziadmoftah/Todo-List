from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from entities.task import Task
from entities.subtask import Subtask
from entities.priority import Priority
from todos.subtasks import services as subtask_services
from todos.subtasks.models import SubtaskGet
from todos.tasks.models import TaskCreate, TaskGet, TaskEdit
from utils.pagination import Pagination


def get_task_by_task_id(db : Session, task_id : int, pagination: Pagination) :
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
    db_subtask = subtask_services.get_subtasks_by_task_id(db , task_id , pagination)
    return TaskGet(subtasks=db_subtask, title=db_task.task_title, priority=db_task.priority_title, is_completed=db_task.is_completed)

def create_task(db: Session , task: TaskCreate) -> TaskCreate:
    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    return task

def get_tasks_by_list_id(db: Session, list_id : int) -> List[TaskGet]:
    db_tasks = db.query(
            Task.title.label('task_title'),
            Task.is_completed.label('task_is_completed'),
            Priority.title.label('priority_title'),
            Subtask.title.label('subtask_title'),
            Subtask.is_completed.label('subtask_is_completed')
        ).outerjoin(Subtask, Task.id_task == Subtask.id_task # Equivalent to RIGHT JOIN from subtasks to tasks
        ).join(Priority, Task.id_priority == Priority.id_priority
        ).filter(Task.id_list == list_id
        ).all()

    tasks = {}
    print (db_tasks)
    for (task_title, task_is_completed, priority_title, subtask_title, subtask_is_completed) in db_tasks:
        if task_title not in tasks:
            tasks[task_title] = TaskGet(
                title=task_title,
                is_completed=task_is_completed,
                priority=priority_title,
                subtasks=[]
            )
        if subtask_title is not None and subtask_is_completed is not None:
            tasks[task_title].subtasks.append(SubtaskGet(title=subtask_title,is_completed=subtask_is_completed))
    return list(tasks.values())

def edit_task(db: Session , task_id: int, task: TaskEdit) -> TaskGet:
    if not task.model_fields_set :
        raise HTTPException(HTTP_400_BAD_REQUEST, "Task Edit Request body was empty")
    db_task = db.query(Task).filter(Task.id_task == task_id).first()
    if db_task is None:
        raise HTTPException(HTTP_404_NOT_FOUND, "Task is not found")
    if task.title is not None:
        db_task.title = task.title
    if task.is_completed is not None:
        db_task.is_completed = task.is_completed
    if task.id_priority is not None:
        db_task.id_priority = task.id_priority
    db.commit()
    db.refresh(db_task)
    return TaskGet(title=db_task.title,
                      is_completed=db_task.is_completed,
                      priority=(db.query(Priority.title).filter(Priority.id_priority == db_task.id_priority).first()).title,
                      subtasks= subtask_services.get_subtasks_by_task_id(db, task_id))

def delete_task(db: Session, task_id: int):
    deleted_tasks_count = db.query(Task).filter(Task.id_task == task_id).delete()
    if deleted_tasks_count == 0:
        raise HTTPException(HTTP_400_BAD_REQUEST, "No task found for given task_id")
    subtask_services.delete_subtasks_by_task_id(db , task_id)
    db.commit()