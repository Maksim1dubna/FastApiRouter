from fastapi import APIRouter
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

@router.get("/create")
async def create_user():
    pass

@router.get("/update")
async def update_user():
    pass

@router.get("/delete")
async def delete_user():
    pass
