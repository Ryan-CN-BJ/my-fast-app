from pydantic import BaseModel, Field

from userservice.model.product import (
    MAX_BRAND_LENGTH,
    MAX_DESCRIPTION_LENGTH,
    MAX_NAME_LENGTH,
)
from typing import Annotated
from userservice.schema.sku import ResponseSku
from userservice.schema.category import ResponseCategory


class CreateProduct(BaseModel):
    brand: Annotated[str, Field(max_length=MAX_BRAND_LENGTH)]
    name: Annotated[str, Field(max_length=MAX_NAME_LENGTH)]
    description: Annotated[str, Field(max_length=MAX_DESCRIPTION_LENGTH)]


class ResponseProduct(BaseModel):
    id: int
    brand: Annotated[str, Field(max_length=MAX_BRAND_LENGTH)]
    name: Annotated[str, Field(max_length=MAX_NAME_LENGTH)]
    description: Annotated[str, Field(max_length=MAX_DESCRIPTION_LENGTH)]

    model_config = {"from_attributes": True}


class ResponseProductWithSkus(ResponseProduct):
    skus: list[ResponseSku]


class ResponseProductWithCates(ResponseProduct):
    cates: list[ResponseCategory]
