from fastapi import APIRouter

router = APIRouter(prefix="/task", tags=["task"])

@router.get("/")
async def all_task():
    pass

@router.get("/task_id")
async def task_by_id():
    pass

@router.get("/create")
async def create_task():
    pass

@router.get("/update")
async def update_task():
    pass

@router.get("/delete")
async def delete_task():
    pass