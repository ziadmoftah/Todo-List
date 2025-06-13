from pydantic import BaseModel
from todos.subtasks.models import SubtaskGet

class TaskCreate(BaseModel):
    title: str
    is_completed: bool = False
    id_priority: int
    id_list: int

class TaskGet(BaseModel):
    title: str
    is_completed: bool
    priority: str
    subtasks: list[SubtaskGet]

class TaskEdit(BaseModel):
    title: str = None
    is_completed: bool = None
    id_priority: int = None


