from pydantic import BaseModel
from todos.subtasks.models import NewSubtaskGet

class NewTaskCreate(BaseModel):
    title: str
    is_completed: bool = False
    id_priority: int
    id_list: int

class NewTaskGet(BaseModel):
    title: str
    is_completed: bool
    priority: str
    subtasks: list[NewSubtaskGet]

class NewSubtaskEdit(BaseModel):
    title: str = None
    is_completed: bool = None
    id_priority: int = None


