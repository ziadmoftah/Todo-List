from fastapi import FastAPI
from routers import subtask_controller, task_controller, list_controller




app = FastAPI(title="Todo list")
app.include_router(list_controller.router)
app.include_router(task_controller.router)
app.include_router(subtask_controller.router)




@app.get("/HelloWorld")
def read_root():
    return {"Hello World"}





