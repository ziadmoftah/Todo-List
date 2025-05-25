from fastapi import APIRouter, HTTPException, status
from typing import List
from models.subtask_dao import get_subtask_data, delete_subtask, create_subtasks
from schemas.subtask_schema import SubtaskCreate, SubtaskGet
from sql_conncetion import get_sql_connection

connection = get_sql_connection()

router = APIRouter(
    tags=["Subtasks"], # Group these endpoints in Swagger UI
    prefix="/subtask"
)

@router.get("/{subtask_id}/get", response_model=SubtaskGet)
def read_subtask(subtask_id: int):
    data = get_subtask_data(connection, subtask_id)
    response = SubtaskGet(title="",is_completed=False)
    for (subtask_title, subtask_status) in data:
        response.title = subtask_title
        response.is_completed = subtask_status
    return response


@router.post("/create")
def create_subtask(subtasks_data: List[SubtaskCreate]):
    data = []
    for subtask in subtasks_data:
        data.append([subtask.task_id , subtask.title])
    create_subtasks(connection , data)
    return {"Subtasks created successfully"}

# @app.post("/subtask/{subtask_id}/edit")
# def edit_subtask(subtask_id : int , subtask_data):
#     pass

@router.post("/{subtask_id}/delete")
def remove_subtask(subtask_id : int):
    delete_subtask(connection , subtask_id)
    return {f"Subtask {subtask_id} was removed successfully"}