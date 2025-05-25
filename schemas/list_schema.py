from pydantic import BaseModel
from schemas.task_schema import TaskGet


class ListGet(BaseModel):
    title: str
    priority: str
    tasks: list[TaskGet]