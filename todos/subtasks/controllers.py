from typing import List
from fastapi import APIRouter
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT
from database.core import DbSession
from todos.subtasks.models import SubtaskCreate, SubtaskGet, SubtaskEdit
from todos.subtasks import services

router = APIRouter(
    tags=["Subtasks"], # Group these endpoints in Swagger UI
    prefix="/subtasks"
)

@router.post("/create" , status_code=HTTP_201_CREATED, response_model=List[SubtaskCreate] )
def create_subtask(db : DbSession , subtask : List[SubtaskCreate]):
    return services.create_subtasks(db , subtask)

@router.get("/{subtask_id}/get" , status_code=HTTP_200_OK, response_model=SubtaskGet)
def get_subtask(db : DbSession, subtask_id : int):
    return services.get_subtask_by_subtask_id(db , subtask_id)

@router.post("/{subtask_id}/edit", status_code=HTTP_200_OK)
def edit_Subtask(db: DbSession, subtask_id: int , subtask : SubtaskEdit):
    return services.edit_subtask(db , subtask_id, subtask)

@router.post("/{subtask_id}/delete", status_code=HTTP_204_NO_CONTENT)
def delete_Subtask(db: DbSession, subtask_id: int ):
    return services.delete_subtask(db, subtask_id)