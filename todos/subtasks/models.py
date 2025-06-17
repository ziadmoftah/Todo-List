from pydantic import BaseModel

class SubtaskCreate(BaseModel):
    title: str
    is_completed: bool = False
    id_task: int

class SubtaskGet(BaseModel):
    title: str
    is_completed: bool = False

class SubtaskEdit(BaseModel):
    title: str | None = None
    is_completed: bool | None = None