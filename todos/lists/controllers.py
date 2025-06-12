from fastapi import APIRouter
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT
from database.core import DbSession
from todos.lists.models import NewListGet, NewListCreate, NewListEdit
from todos.lists import services

router = APIRouter(
    tags=["New Lists"], # Group these endpoints in Swagger UI
    prefix="/NewLists"
)

@router.get("/{list_id}/get", status_code=HTTP_200_OK , response_model=NewListGet)
def get_list_data(db : DbSession, list_id: int):
    return services.get_list_data(db , list_id)

@router.post("/create", status_code= HTTP_201_CREATED, response_model=NewListCreate)
def create_list(db: DbSession, list: NewListCreate):
    return services.create_list(db , list)

@router.post("{list_id}/edit", status_code=HTTP_200_OK, response_model=NewListCreate)
def edit_list(db:DbSession, list_id: int, list: NewListEdit):
    return services.edit_list(db , list_id, list)

@router.post("{list_id}/delete", status_code=HTTP_204_NO_CONTENT)
def delete_list(db: DbSession , list_id):
    return "Not implemented yet"

