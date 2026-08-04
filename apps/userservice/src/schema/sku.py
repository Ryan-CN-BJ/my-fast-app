from pydantic import BaseModel
from decimal import Decimal


class CreateSku(BaseModel):
    product_id: int
    sku_code: str
    price: Decimal
    stock: int
    attrs: dict
    image_url: str
