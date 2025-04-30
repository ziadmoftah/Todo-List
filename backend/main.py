from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from sql_conncetion import get_sql_connection
from task_dao import get_task_subtask_data, get_all_task_subtask_data
from subtask_dao import get_subtask_date, create_subtasks
from list_dao import get_all_todo_list_data

app = FastAPI()
connection = get_sql_connection()


class SubtaskCreate(BaseModel):
    task_id : int
    title: str
    is_completed: Optional[bool] = None

class SubtaskUpdate(BaseModel):
    title: Optional[str] = None
    is_completed: Optional[bool] = None

@app.get("/HelloWorld")
def read_root():
    return {"Hello": "World"}



@app.get("list/get")
def get_all_lists_data():
    pass

@app.get("/task/{task_id}/subtasks/get")
def get_subtask_data_by_task_id(task_id : int):
    data = get_task_subtask_data(connection, task_id)
    response = []
    for (subtask_title, subtask_status ) in data:
        response.append({
            'title': subtask_title,
            'status' : "Done" if subtask_status else "Todo"
        })
    return response

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
        task_entry["Subtasks"].append({
            "title": subtask_title,
            "status": "Completed" if subtask_status else "Todo"
        })
    return response

@app.get("/subtask/{subtask_id}/get")
def get_subtask_data_by_subtask_id(subtask_id: int):
    data = get_subtask_date(connection, subtask_id)
    if len(data) == 0:
        return {"Sorry subtask not found"}
    response = []
    for (subtask_title, subtask_status) in data:
        response.append({
            'title': subtask_title,
            'status': "Done" if subtask_status else "Todo"
        })
    return response

@app.post("/task/{task_id}/subtask/create")
def create_subtask(subtasks_data: List[SubtaskCreate]):
    data = []
    for subtask in subtasks_data:
        data.append([subtask.task_id , subtask.title])
    print(data)

    create_subtasks(connection , data)

    return {"Subtasks created successfully"}

@app.post("/subtask/{subtask_id}/edit")
def edit_subtask(subtask_id : int , subtask_data: SubtaskUpdate):
    pass


