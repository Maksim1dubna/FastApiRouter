from app.routers.users import User
from app.routers.task import Task

from sqlalchemy.schema import CreateTable
print(CreateTable(Task.__table__))
print(CreateTable(User.__table__))
