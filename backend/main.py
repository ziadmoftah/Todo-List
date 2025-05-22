from fastapi import FastAPI
from typing import List
from routers import subtask_controller, task_controller
from sql_conncetion import get_sql_connection
from models.task_dao import get_task_subtask_data, get_all_task_subtask_data, Task, create_tasks, get_task_data



app = FastAPI(title="Todo list")
app.include_router(subtask_controller.router)
app.include_router(task_controller.router)
connection = get_sql_connection()



@app.get("/HelloWorld")
def read_root():
    return {"Hello World"}





