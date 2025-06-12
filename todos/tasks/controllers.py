from typing import List
from fastapi import  APIRouter
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from database.core import DbSession
from todos.tasks import services
from todos.tasks.models import NewTaskGet, NewTaskCreate, NewSubtaskEdit

router = APIRouter(
    tags=["NewTasks"], # Group these endpoints in Swagger UI
    prefix="/NewTasks"
)

@router.get("/{task_id}/get" , status_code=HTTP_200_OK, response_model=NewTaskGet)
def getNewTaskData(db : DbSession,task_id : int):
    return services.get_task_by_task_id(db , task_id)

@router.post("/create", status_code=HTTP_201_CREATED, response_model=NewTaskCreate)
def create_task(db: DbSession, task : NewTaskCreate):
    return services.create_task(db , task)

@router.get("/{list_id}/tasks", status_code=HTTP_200_OK , response_model=List[NewTaskGet])
def get_tasks_by_list_id(db: DbSession, list_id : int):
    return services.get_tasks_by_list_id(db, list_id)

@router.post("/{task_id}/edit", status_code= HTTP_200_OK , response_model=NewTaskGet)
def edit_task(db: DbSession , task_id: int, task: NewSubtaskEdit):
    return services.edit_task(db, task_id, task)

@router.post("/{task_id}/delete", status_code= HTTP_204_NO_CONTENT)
def delete_task(db: DbSession , task_id: int):
    return services.delete_task(db , task_id)