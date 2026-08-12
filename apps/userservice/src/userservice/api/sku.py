from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession
from apps.userservice.src.userservice.core.db import get_db
from typing import Annotated
from apps.userservice.src.userservice.schema.sku import CreateSku
from apps.userservice.src.userservice.service.sku_service import SkuService, ResponseSku
from apps.userservice.src.userservice.schema.response import ApiResponse

router = APIRouter(prefix="/sku")


@router.post("/add", response_model=ApiResponse[ResponseSku])
async def add_sku(
    db: Annotated[AsyncSession, Depends(get_db)], data: Annotated[CreateSku, Body(...)]
):
    sku_service = SkuService(db)
    sku = await sku_service.add_sku(data)
    return ApiResponse(data=sku)
