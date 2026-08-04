from fastapi import APIRouter, Depends, Body

from schema.product import ResponseProduct, CreateProduct
from schema.response import ApiResponse

from service.product_service import ProductService
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from core.db import get_db

router = APIRouter(prefix="/product")


@router.post("/add", response_model=ApiResponse[ResponseProduct])
async def add_product(
    db: Annotated[AsyncSession, Depends(get_db)],
    product: Annotated[CreateProduct, Body(..., description="新增产品入参")],
):
    product_service = ProductService(db)
    res = await product_service.add_product(product)
    return ApiResponse(data=res)
