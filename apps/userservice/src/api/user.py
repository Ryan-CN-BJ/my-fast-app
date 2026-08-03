from fastapi import APIRouter, Query, Body, Depends
from service.user_service import UserService
from core.db import get_db
from schema.user import UserRegister

from sqlalchemy.ext.asyncio import AsyncSession

from schema.response import ApiResponse, PageResponse, PageData
from schema.user import UserResponse

from model.user import User


from sqlalchemy import select, func
from typing import Annotated
from fastapi.exceptions import HTTPException

router = APIRouter(prefix="/user")


@router.post(
    "/register",
    response_model=ApiResponse[UserResponse],
)
async def register_user(
    data: Annotated[UserRegister, Body(..., description="用户注册信息")],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    raise HTTPException(404, "Forbidden")
    userservice = UserService(db)
    useResponse = await userservice.regiser_user(data)
    return ApiResponse(data=useResponse)


@router.get(
    "/query",
    response_model=ApiResponse[UserResponse],
)
async def get_user_by_id(
    id: Annotated[int, Query(..., description="用户id")],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    userservice = UserService(db)
    useResponse: UserResponse = await userservice.get_user_by_id(id)
    return ApiResponse(data=useResponse)


@router.get("/all", response_model=PageResponse[UserResponse])
async def get_users(
    db: Annotated[AsyncSession, Depends(get_db)],
    page: Annotated[int, Query(description="页码")] = 1,
    size: Annotated[int, Query(description="页容量")] = 10,
    name: Annotated[str | None, Query(description="名字")] = None,
):
    userservice = UserService(db)
    users = await userservice.get_all_user(page, size, name)
    print("users", users)
    result = [{"id": u.id, "name": u.name, "email": u.email} for u in users]
    total = await db.scalar(
        select(func.count(User.id)).where(User.name.ilike(f"%{name}%"))
    )
    data = PageData(
        records=result, page=page, size=size, total=0 if total is None else total
    )
    return PageResponse(data=data)


async def del_user_by_id(
    db: Annotated[AsyncSession, Depends(get_db)],
    id: Annotated[str, Query(description="用户id")],
):
    userService = UserService(db)
    await userService.del_user(id)
    return ApiResponse()
