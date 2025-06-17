from typing import List, Annotated
from fastapi import  APIRouter
from fastapi.params import Depends
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from database.core import DbSession
from todos.subtasks.models import SubtaskGet
from todos.tasks import services
from todos.subtasks import services as subtask_services
from todos.tasks.models import TaskGet, TaskCreate, TaskEdit
from utils.pagination import Pagination, pagination_param

router = APIRouter(
    tags=["Tasks"], # Group these endpoints in Swagger UI
    prefix="/tasks"
)

@router.get("/{task_id}/get" , status_code=HTTP_200_OK, response_model=TaskGet)
def get_task_data(db : DbSession,task_id : int, pagination: Annotated[Pagination, Depends(pagination_param)]):
    return services.get_task_by_task_id(db , task_id, pagination)

@router.get("/{task_id}/subtasks" , status_code=HTTP_200_OK, response_model=List[SubtaskGet])
def get_subtasks_by_task_id(db : DbSession, task_id : int , pagination: Annotated[Pagination, Depends(pagination_param)]):
    return subtask_services.get_subtasks_by_task_id(db , task_id , pagination)

@router.post("/create", status_code=HTTP_201_CREATED, response_model=TaskCreate)
def create_task(db: DbSession, task : TaskCreate):
    return services.create_task(db , task)

@router.post("/{task_id}/edit", status_code= HTTP_200_OK , response_model=TaskGet)
def edit_task(db: DbSession , task_id: int, task: TaskEdit):
    return services.edit_task(db, task_id, task)

@router.post("/{task_id}/delete", status_code= HTTP_204_NO_CONTENT)
def delete_task(db: DbSession , task_id: int):
    return services.delete_task(db , task_id)