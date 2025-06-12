from fastapi import FastAPI
from entities import subtask,task,priority,list
from routers import subtask_controller, task_controller, list_controller
from database.core import  engine
from todos.subtasks import controllers as new_subtask_controllers
from todos.tasks import controllers as new_task_controllers
from todos.lists import controllers as new_list_controllers
from database.core import DbSession



app = FastAPI(title="Todo list")
subtask.Base.metadata.create_all(bind=engine)
task.Base.metadata.create_all(bind=engine)
priority.Base.metadata.create_all(bind=engine)
list.Base.metadata.create_all(bind=engine)


app.include_router(list_controller.router)
app.include_router(task_controller.router)
app.include_router(subtask_controller.router)
app.include_router(new_subtask_controllers.router)
app.include_router(new_task_controllers.router)
app.include_router(new_list_controllers.router)


@app.get("/HelloWorld")
def read_root():
    return {"Hello World"}





