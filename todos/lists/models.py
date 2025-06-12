from typing import List
from pydantic import BaseModel
from todos.tasks.models import NewTaskGet


class NewListCreate(BaseModel):
    title: str
    id_priority: int

class NewListGet(BaseModel):
    title: str
    priority: str
    tasks: List[NewTaskGet]

class NewListEdit(BaseModel):
    title: str = None
    id_priority: int = None
