# cd app
# python -m uvicorn app.routers.main:app
# alembic revision --autogenerate -m "Initial migration"
# alembic upgrade head

from fastapi import FastAPI
from app.models import users, task

app = FastAPI()

@app.get("/")
async def welcome() -> dict:
    return {"message": "Welcome to Taskmanager"}

app.include_router(users.router)
app.include_router(task.router)
