from fastapi import APIRouter, Depends, status, HTTPException
from slugify import slugify
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from app.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from app.routers.schemas import CreateUser
# Функции работы с записями.
from sqlalchemy import insert, select, update
# Функция создания slug-строки

from app.backend.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

router = APIRouter(prefix="/user", tags=["user"])

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    username = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    age = Column(Integer)
    slug = Column(String, unique=True, index=True)
    tasks = relationship("Task", back_populates='user')

@router.get("/")
async def all_task(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User).where(User.is_active == True)).all()
    return users

@router.get("/user_id")
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.post("/create")
async def create_user(db: Annotated[Session, Depends(get_db)], create_user: CreateUser):
    db.execute(insert(User).values(
                                   username = create_user.username,
                                   firstname = create_user.firstname,
                                   lastname = create_user.lastname,
                                   age = create_user.age,
                                   slug = slugify(create_user.username)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'}

@router.put("/update")
async def update_user(db: Annotated[Session, Depends(get_db)], user_id: int, update_user: CreateUser):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nothing found to update")
    db.execute(update(User).where(User.id == user_id).values(
        username = update_user.username,
        firstname = update_user.firstname,
        lastname = update_user.lastname,
        age = update_user.age,
        slug = slugify(create_user.username)))
    db.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'Updated'}

@router.delete("/delete")
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nothing found to delete"
        )
    db.execute(update(User).where(User.id == user_id).values(is_active = False))
    db.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'Deleted'}
