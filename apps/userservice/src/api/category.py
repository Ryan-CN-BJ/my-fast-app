from fastapi import APIRouter, Body, Depends
from schema.response import ApiResponse
from schema.category import ResponseCategory, CreateCategory
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import get_db
from service.category_service import CategoruService

router = APIRouter(prefix="/cate")


@router.post("/add", response_model=ApiResponse[ResponseCategory])
async def add_category(
    category: Annotated[CreateCategory, Body(...)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    category_service = CategoruService(db)
    res = await category_service.add_category(category)
    return ApiResponse(data=res)
