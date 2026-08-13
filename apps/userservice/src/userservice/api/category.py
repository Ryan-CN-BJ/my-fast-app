from fastapi import APIRouter, Body, Depends
from userservice.schema.response import ApiResponse
from userservice.schema.category import (
    ResponseCategory,
    CreateCategory,
)
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from userservice.core.db import get_db
from userservice.service.category_service import CategoruService

router = APIRouter(prefix="/cate")


@router.post("/add", response_model=ApiResponse[ResponseCategory])
async def add_category(
    category: Annotated[CreateCategory, Body(...)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    category_service = CategoruService(db)
    res = await category_service.add_category(category)
    return ApiResponse(data=res)
