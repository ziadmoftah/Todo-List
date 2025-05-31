from fastapi import APIRouter, HTTPException, status
from typing import List

from schemas.subtask_schema import SubtaskGet
from schemas.task_schema import TaskGet
from sql_conncetion import get_sql_connection
from models import list_dao
from schemas.list_schema import ListGet, ListCreate

connection = get_sql_connection()

router = APIRouter(
    tags=["Lists"], # Group these endpoints in Swagger UI
    prefix="/lists"
)

@router.get("/{list_id}/get", response_model=ListGet)
def get_single_list_data(list_id: int):
    data = list_dao.get_all_todo_list_data(connection, list_id)
    tasks = {}
    for (list_title, list_priority, task_title, task_priority, task_is_completed, subtask_title, subtask_is_completed) in data:
        if task_title not in tasks:
            tasks[task_title]= TaskGet(
                title=task_title,
                priority=task_priority,
                is_completed=task_is_completed,
                subtasks=[]
            )
        tasks[task_title].subtasks.append(SubtaskGet(
            title=subtask_title,
            is_completed=subtask_is_completed
        ))

    response = ListGet(
        title=data[0][0],
        priority=data[0][1],
        tasks=list(tasks.values())
    )

    return response


@router.post("/create")
def create_list(list: ListCreate):
    list_dao.create_list(connection, list)
