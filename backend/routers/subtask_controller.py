from fastapi import APIRouter, HTTPException, status
from typing import List
from models.subtask_dao import get_subtask_data, delete_subtask, create_subtasks, Subtask
from sql_conncetion import get_sql_connection

connection = get_sql_connection()

router = APIRouter(
    tags=["Subtasks"], # Group these endpoints in Swagger UI
    responses={404: {"description": "Not found"}},
)

@router.get("/subtask/{subtask_id}/get")
def read_subtask(subtask_id : int):
    data = get_subtask_data(connection , subtask_id)
    response = []
    for (subtask_title, subtask_status) in data:
        response.append({
            'title': subtask_title,
            'status': "Done" if subtask_status else "Todo"
        })
    return response


@router.post("/subtask/create")
def create_subtask(subtasks_data: List[Subtask]):
    data = []
    for subtask in subtasks_data:
        data.append([subtask.task_id , subtask.title])
    create_subtasks(connection , data)
    return {"Subtasks created successfully"}

# @app.post("/subtask/{subtask_id}/edit")
# def edit_subtask(subtask_id : int , subtask_data):
#     pass

@router.post("/subtask/{subtask_id}/delete")
def remove_subtask(subtask_id : int):
    delete_subtask(connection , subtask_id)
    return {f"Subtask {subtask_id} was removed successfully"}