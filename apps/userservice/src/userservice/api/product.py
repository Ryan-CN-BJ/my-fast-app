from fastapi import APIRouter, Depends, Body, Query

from userservice.schema.product import (
    ResponseProduct,
    CreateProduct,
    ResponseProductWithSkus,
    ResponseProductWithCates,
)
from userservice.schema.response import ApiResponse

from userservice.service.product_service import ProductService
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from userservice.core.db import get_db

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
    productWithSkus = await productService.get_product_with_sku(id)
    return ApiResponse(data=productWithSkus)


@router.get(
    "/query/productwithcates", response_model=ApiResponse[ResponseProductWithCates]
)
async def get_product_width_skus(
    db: Annotated[AsyncSession, Depends(get_db)],
    id: Annotated[int, Query(..., description="产品id")],
):
    product_service = ProductService(db)
    res = await product_service.get_product_with_cate(id)
    return ApiResponse(data=res)


@router.post("/updatecates", response_model=ApiResponse[ResponseProductWithCates])
async def add_category_to_prodcut(
    db: Annotated[AsyncSession, Depends(get_db)],
    cate_ids: Annotated[list[int], Body(..., min_length=1, description="商品种类id")],
    product_id: Annotated[int, Body(..., description="商品id")],
):
    product_service = ProductService(db)
    res = await product_service.update_product_cates(
        product_id=product_id, cate_ids=cate_ids
    )
    return ApiResponse(data=res)
