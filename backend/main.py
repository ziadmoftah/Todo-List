from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from sql_conncetion import get_sql_connection
from task_dao import get_task_subtask_data, get_all_task_subtask_data, Task, create_tasks, get_task_data
from subtask_dao import create_subtasks, delete_subtask, Subtask


app = FastAPI()
connection = get_sql_connection()



@app.get("/HelloWorld")
def read_root():
    return {"Hello World"}


@app.get("/task/{task_id}/get")
def get_all_task_data(task_id : int):
    response = []
    task_data = get_task_data(connection , task_id)
    subtask_data = get_task_subtask_data(connection, task_id)
    for (task_title, task_is_completed, task_priority) in task_data:
        response.append({
            "Task title" : task_title,
            "Task status" : "Done" if task_is_completed else "Todo",
            "Task priority" : task_priority
        })
    for (subtask_title, subtask_status) in subtask_data:
        response.append({
            'title': subtask_title,
            'status': "Done" if subtask_status else "Todo"
        })
    return response


@app.post("/task/create")
def create_task(task : Task):
    create_tasks(connection , task)
    return {"Task created successfully"}

@app.get("/task/all_data")
def get_all_tasks():
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


@app.get("/task/{task_id}/subtasks/get")
def get_all_subtasks_by_task_id(task_id : int):
    data = get_task_subtask_data(connection, task_id)
    response = []
    for (subtask_title, subtask_status) in data:
        response.append({
            'title': subtask_title,
            'status': "Done" if subtask_status else "Todo"
        })
    return response


@app.post("/subtask/create")
def create_subtask(subtasks_data: List[Subtask]):
    data = []
    for subtask in subtasks_data:
        data.append([subtask.task_id , subtask.title])
    create_subtasks(connection , data)
    return {"Subtasks created successfully"}

# @app.post("/subtask/{subtask_id}/edit")
# def edit_subtask(subtask_id : int , subtask_data):
#     pass

@app.post("/subtask/{subtask_id}/delete")
def remove_subtask(subtask_id : int):
    delete_subtask(connection , subtask_id)
    return {f"Subtask {subtask_id} was removed successfully"}



