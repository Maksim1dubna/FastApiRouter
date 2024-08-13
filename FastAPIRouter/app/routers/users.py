from fastapi import APIRouter

router = APIRouter(prefix="/user", tags=["user"])

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