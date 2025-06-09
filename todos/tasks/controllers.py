from typing import List

from fastapi import  APIRouter
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
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
def get_all_tasks_data(db: DbSession, list_id : int):
    return services.get_tasks_by_list_id(db, list_id)


