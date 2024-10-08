from pydantic import BaseModel

class CreateUser(BaseModel):
    username: str
    firstname: str
    lastname: str
    age: int


class UpdateUser(BaseModel):
    firstname: str
    lastname: str
    age: int


class CrateTask(BaseModel):
    title: str
    content: str
    priority: int
    user_id: int


class UpdateTask(BaseModel):
    title: str
    content: str
    priority: int
    user_id: int
