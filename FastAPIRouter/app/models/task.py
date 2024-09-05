from fastapi import APIRouter, Depends, status, HTTPException
import slugify
# Сессия БД
from sqlalchemy.orm import Session

import app.models.users
# Функция подключения к БД
from app.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from app.routers.schemas import CrateTask
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки

from app.backend.db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
# from app.models.users import User

router = APIRouter(prefix="/task", tags=["task"])

class Task(Base):
    __tablename__ = 'tasks'
    __table_args__ = {"keep_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    priority = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    slug = Column(String, unique=True, index=True)
    user = relationship("User", back_populates='tasks')

@router.get("/")
async def all_task(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks

@router.get("/task_id")
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalar(select(Task).where(task_id == Task.id))
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return task

@router.post("/create_task")
async def create_task(db: Annotated[Session, Depends(get_db)], create_task: CrateTask):
    user = db.scalar(select(app.models.users.User).where(create_task.user_id == app.models.users.User.id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This user doesnt exist")
    db.execute(insert(Task).values(
        title = create_task.title,
        content = create_task.content,
        priority = create_task.priority,
        user_id = create_task.user_id,
        slug=slugify.slugify(create_task.title)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'}

@router.put("/update_task")
async def update_task(db: Annotated[Session, Depends(get_db)], task_id: int, update_task: CrateTask):
    user = db.scalar(select(Task).where(task_id == Task.id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nothing found to update")
    db.execute(update(Task).where(task_id == Task.id).values(
        title = update_task.title,
        content = update_task.content,
        priority = update_task.priority,
        slug = slugify.slugify(update_task.title)))
    db.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'Updated'}


@router.delete("/delete_task")
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    user = db.scalar(select(Task).where(task_id == Task.id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nothing found to delete"
        )
    db.execute(delete(Task).where(task_id == Task.id))
    db.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'Deleted'}
