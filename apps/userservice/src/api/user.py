from fastapi import APIRouter, Query, Body, Depends
from service.user_service import UserService
from core.db import get_db
from schema.user import UserRegister

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/user")


@router.get("/")
def get_user(size: int = Query(default=10), page: int = Query(default=1)):
    print(size, page)
    return {"code": 200}


@router.post("/add")
def add_user(
    email: str = Body(..., min_length=1, max_length=10, description="邮箱不能为空!"),
    name: str = Body(..., min_length=1, max_length=10, description="姓名不能为空!"),
):
    return {"code": 200, "data": {"email": email, "name": name}}


@router.post("/register")
async def register_user(
    data: UserRegister = Body(..., description="用户注册信息"),
    db: AsyncSession = Depends(get_db),
):
    userservice = UserService(db)
    return await userservice.regiser_user(data)
