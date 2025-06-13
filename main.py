from fastapi import FastAPI
from apis import register_routes
from database.core import  engine, Base



app = FastAPI(title="Todo list")
Base.metadata.create_all(bind=engine)
register_routes(app)