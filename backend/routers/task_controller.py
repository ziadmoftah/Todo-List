from sql_conncetion import get_sql_connection
from models.task_dao import get_task_subtask_data, get_all_task_subtask_data, Task, create_tasks, get_task_data
from fastapi import FastAPI, APIRouter
from typing import List


connection = get_sql_connection()


router = APIRouter(
    tags=["Tasks"], # Group these endpoints in Swagger UI
    responses={404: {"description": "Not found"}},
)


@router.get("/task/{task_id}/get")
def get_single_task_data(task_id : int):
    response = {
        "Task title": "",
        "Task status": "",
        "Task priority": "",
        "Subtasks": []
    }
    task_data = get_task_data(connection , task_id)
    subtask_data = get_task_subtask_data(connection, task_id)
    #print(task_data)
    for (task_title, task_is_completed, task_priority) in task_data:
        response["Task title"] = task_title
        response["Task status"] = "Done" if task_is_completed else "Todo"
        response["Task priority"] = task_priority
    for (subtask_title, subtask_status) in subtask_data:
        response["Subtasks"].append({
            'title': subtask_title,
            'status': "Done" if subtask_status else "Todo"
        })
    return response



@router.post("/task/create")
def create_task(task : Task):
    create_tasks(connection , task)
    return {"Task created successfully"}

@router.get("/task/all_data")
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


