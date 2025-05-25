from fastapi import APIRouter, HTTPException, status
from typing import List
from sql_conncetion import get_sql_connection
from models.list_dao import get_all_todo_list_data
from schemas.list_schema import ListGet
connection = get_sql_connection()

router = APIRouter(
    tags=["Lists"], # Group these endpoints in Swagger UI
    prefix="/list"
)

@router.get("/{list_id}/get" , response_model=ListGet)
def get_single_list_data(list_id : int):
    return "HEllO"
    data = get_all_todo_list_data(connection , list_id)
    response = ListGet(title="", priority="" , tasks=[])
    for (list_title, list_priority, task_title, task_priority, task_is_completed, subtask_title, subtask_is_completed) in data:
        pass
    return ListGet()