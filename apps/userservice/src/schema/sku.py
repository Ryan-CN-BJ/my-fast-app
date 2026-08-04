from pydantic import BaseModel, Field
from decimal import Decimal

from typing import Annotated
from model.sku import MAX_SKU_CODE_LENGTH, MAX_PRICE_DIGITS, PRICE_DECIMAL_PLACES


class CreateSku(BaseModel):
    product_id: int
    sku_code: Annotated[str, Field(max_length=MAX_SKU_CODE_LENGTH)]
    price: Annotated[
        Decimal, Field(max_digits=MAX_PRICE_DIGITS, decimal_places=PRICE_DECIMAL_PLACES)
    ]
    stock: int
    attrs: dict
    image_url: str
