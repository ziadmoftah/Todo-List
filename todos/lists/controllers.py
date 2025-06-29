from typing import List
from fastapi import APIRouter
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT

from auth.services import CurrentUser
from database.core import DbSession
from todos.lists.models import ListGet, ListCreate, ListEdit
from todos.lists import services
from todos.tasks import services as task_services
from todos.tasks.models import TaskGet

router = APIRouter(
    tags=["Lists"], # Group these endpoints in Swagger UI
    prefix="/lists"
)

@router.post("/get" , status_code=HTTP_200_OK , response_model= List[ListGet])
def get_all_lists_data(db: DbSession, user: CurrentUser):
    return services.get_all_lists_data(db, user)

@router.get("/{list_id}/get", status_code=HTTP_200_OK , response_model=ListGet)
def get_list_data(db : DbSession, list_id: int):
    return services.get_list_data(db , list_id)

@router.get("/{list_id}/tasks", status_code=HTTP_200_OK , response_model=List[TaskGet])
def get_tasks_by_list_id(db: DbSession, list_id : int):
    return task_services.get_tasks_by_list_id(db, list_id)

@router.post("/create", status_code= HTTP_201_CREATED, response_model=ListCreate)
def create_list(db: DbSession, list: ListCreate):
    return services.create_list(db , list)

@router.post("{list_id}/edit", status_code=HTTP_200_OK, response_model=ListCreate)
def edit_list(db:DbSession, list_id: int, list: ListEdit):
    return services.edit_list(db , list_id, list)

@router.post("{list_id}/delete", status_code=HTTP_204_NO_CONTENT)
def delete_list(db: DbSession , list_id):
    return "Not implemented yet"

