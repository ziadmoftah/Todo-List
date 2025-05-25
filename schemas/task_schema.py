from pydantic import BaseModel
from schemas.subtask_schema import SubtaskGet


class TaskCreate(BaseModel):
    title: str
    is_completed: bool = False
    priority_id: int
    list_id: int


class TaskGet(BaseModel):
    title: str
    is_completed: bool
    priority: str
    subtasks: list[SubtaskGet]