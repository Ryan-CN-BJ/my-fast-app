from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import get_db
from typing import Annotated
from schema.sku import CreateSku
from service.sku_service import SkuService, ResponseSku
from schema.response import ApiResponse

router = APIRouter(prefix="/sku")


@router.post("/add", response_model=ApiResponse[ResponseSku])
async def add_sku(
    db: Annotated[AsyncSession, Depends(get_db)], data: Annotated[CreateSku, Body(...)]
):
    sku_service = SkuService(db)
    sku = await sku_service.add_sku(data)
    return ApiResponse(data=sku)
