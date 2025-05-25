from pydantic import BaseModel

class SubtaskCreate(BaseModel):
    task_id : int
    title: str
    is_completed: bool = False

class SubtaskGet(BaseModel):
    title: str
    is_completed: bool