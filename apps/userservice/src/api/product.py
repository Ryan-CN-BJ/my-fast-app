from fastapi import APIRouter, Depends, Body, Query

from schema.product import ResponseProduct, CreateProduct, ResponseProductWithSkus
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


@router.get(
    "/query/productwithskus", response_model=ApiResponse[ResponseProductWithSkus]
)
async def get_product_with_skus(
    db: Annotated[AsyncSession, Depends(get_db)],
    id: Annotated[int, Query(..., description="产品id")],
):
    productService = ProductService(db)
    productWithSkus = await productService.get_product_width_sku(id)
    return ApiResponse(data=productWithSkus)
