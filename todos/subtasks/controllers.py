from typing import List
from fastapi import APIRouter
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT
from database.core import DbSession
from todos.subtasks.models import NewSubtaskCreate, NewSubtaskGet, NewSubtaskEdit
from todos.subtasks import services

router = APIRouter(
    tags=["NewSubtasks"], # Group these endpoints in Swagger UI
    prefix="/NewSubtasks"
)

@router.post("/createNewSubtask" , status_code=HTTP_201_CREATED )
def createNewSubtask(db : DbSession , subtask : List[NewSubtaskCreate]):
    return services.create_subtasks(db , subtask)

@router.get("/{subtask_id}/getNewSubtask" , status_code=HTTP_200_OK, response_model=NewSubtaskGet)
def getNewSubtask(db : DbSession, subtask_id : int):
    return services.get_subtask_by_subtask_id(db , subtask_id)

@router.get("/{task_id}/GetAllSubtasks" , status_code=HTTP_200_OK, response_model=List[NewSubtaskGet])
def getAllNewSubtasksByTaskId(db : DbSession, task_id : int):
    return services.get_subtasks_by_task_id(db , task_id)

@router.post("/{subtask_id}/editNewSubtask", status_code=HTTP_200_OK)
def editNewSubtask(db: DbSession, subtask_id: int , subtask : NewSubtaskEdit):
    return services.edit_subtask(db , subtask_id, subtask)

@router.post("/{subtask_id}/deleteNewSubtask", status_code=HTTP_204_NO_CONTENT)
def deleteNewSubtask(db: DbSession, subtask_id: int ):
    return services.delete_subtask(db, subtask_id)