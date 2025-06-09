from pydantic import BaseModel
class NewSubtaskCreate(BaseModel):
    title: str
    is_completed: bool = False
    id_task: int


class NewSubtaskGet(BaseModel):
    title: str
    is_completed: bool = False

class NewSubtaskEdit(BaseModel):
    title: str = None
    is_completed: bool = None