from fastapi import APIRouter, Depends, status, HTTPException
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from app.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from app.schemas import CreateUser, UpdateUser
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify

from app.backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship


router = APIRouter(prefix="/user", tags=["user"])

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {"keep_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    age = Column(Integer)
    slug = Column(String, unique=True, index=True)
    tasks = relationship("Task", back_populates='user')
@router.get("/")
async def all_task():
    pass

@router.get("/user_id")
async def user_by_id():
    pass

@router.post("/create")
async def create_user(db: Annotated[Session, Depends(get_db)], create_user: CreateUser):
    db.execute(insert(User).values(
                                   username = create_user.username,
                                   firstname = create_user.firstname,
                                   lastname = create_user.lastname,
                                   age = create_user.age,
                                   slug = slugify(create_user.firstname)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'}

@router.put("/update")
async def update_user():
    pass

@router.delete("/delete")
async def delete_user():
    pass
