from typing import List
from pydantic import BaseModel
from todos.tasks.models import TaskGet


class ListCreate(BaseModel):
    title: str
    id_priority: int

class ListGet(BaseModel):
    title: str
    priority: str
    tasks: List[TaskGet] | None = None

class ListEdit(BaseModel):
    title: str | None = None
    id_priority: int | None = None
