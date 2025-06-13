from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from entities.priority import Priority
from entities.list import List as Todo_List
from todos.lists.models import ListGet, ListCreate, ListEdit
from todos.tasks import services as task_services


def get_list_data(db: Session, list_id: int) -> ListGet:
    db_list = (db.query(Todo_List.title.label("list_title"), Priority.title.label("list_priority"))
               .filter(Todo_List.id_list == list_id)
               .join(Priority , Todo_List.id_priority == Priority.id_priority)
               .first())
    if not db_list:
        raise HTTPException(HTTP_404_NOT_FOUND, "No list found with given list_id")
    return ListGet(title=db_list.list_title , priority=db_list.list_priority , tasks=task_services.get_tasks_by_list_id(db , list_id))

def create_list(db: Session , list: ListCreate) -> ListCreate:
    db_list = Todo_List(**list.model_dump())
    db.add(db_list)
    db.commit()
    return list

def edit_list(db: Session, list_id: int, list: ListEdit) -> ListCreate:
    if not list.model_fields_set :
        raise HTTPException(HTTP_400_BAD_REQUEST, "List Edit Request body was empty")
    db_list = db.query(Todo_List).filter(Todo_List.id_list == list_id).first()
    if db_list is None:
        raise HTTPException(HTTP_404_NOT_FOUND, "List is not found")
    if list.title is not None:
        db_list.title = list.title
    if list.id_priority is not None:
        db_list.is_completed = list.id_priority
    db.commit()
    db.refresh(db_list)
    return ListCreate(title=db_list.title , id_priority=db_list.id_priority)
