from fastapi import FastAPI
from todos.lists import controllers as list_controllers
from todos.tasks import controllers as task_controllers
from todos.subtasks import controllers as subtask_controllers
from auth import controllers as auth_controllers

def register_routes(app : FastAPI):
    app.include_router(auth_controllers.router)
    app.include_router(list_controllers.router)
    app.include_router(task_controllers.router)
    app.include_router(subtask_controllers.router)
