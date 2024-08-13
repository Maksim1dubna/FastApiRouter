# cd app
# python -m uvicorn main:app
from fastapi import FastAPI
from routers import users, task

app = FastAPI()

@app.get("/")
async def welcome() -> dict:
    return {"message": "Welcome to Taskmanager"}

app.include_router(users.router)
app.include_router(task.router)
