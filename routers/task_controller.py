from sql_conncetion import get_sql_connection
from models.task_dao import get_task_subtask_data, get_all_task_subtask_data, create_tasks, get_task_data

from schemas.subtask_schema import SubtaskGet
from schemas.task_schema import TaskCreate, TaskGet
from fastapi import FastAPI, APIRouter
from typing import List


connection = get_sql_connection()


router = APIRouter(
    tags=["Tasks"], # Group these endpoints in Swagger UI
    prefix="/tasks"
)


@router.get("/{task_id}/get" , response_model=TaskGet)
def get_single_task_data(task_id : int):
    response = TaskGet(title="", is_completed=False, priority="", subtasks=[])
    task_data = get_task_data(connection , task_id)
    for (task_title, task_is_completed, task_priority) in task_data:
        response.title = task_title
        response.is_completed = task_is_completed
        response.priority = task_priority

    subtask_data = get_task_subtask_data(connection, task_id)
    for (subtask_title, subtask_status) in subtask_data:
        response.subtasks.append(SubtaskGet(
            title=subtask_title,
            is_completed=subtask_status
        ))
    return response



@router.post("/create")
def create_task(task : TaskCreate):
    create_tasks(connection , task)
    return {"Task created successfully"}

@router.get("/all_data")
def get_all_tasks_data():
    data = get_all_task_subtask_data(connection)
    response = {}
    for task_id, task_title, subtask_title, subtask_status in data:
        task_id = str(task_id)
        # Ensure the main entry exists, defaulting details to an empty list
        task_entry = response.setdefault(task_id, {"Subtasks": []})
        # Set the title only if it hasn't been set yet for this task_id
        if "title" not in task_entry:
            task_entry["title"] = task_title
        # Append the current detail
        if subtask_title:
            task_entry["Subtasks"].append({
                "title": subtask_title,
                "status": "Completed" if subtask_status else "Todo"
            })
    return response


