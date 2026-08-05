from pydantic import BaseModel, Field

from model.product import MAX_BRAND_LENGTH, MAX_DESCRIPTION_LENGTH, MAX_NAME_LENGTH
from typing import Annotated
from schema.sku import ResponseSku


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


class ResponseProductWithSkus(BaseModel):
    id: int
    brand: Annotated[str, Field(max_length=MAX_BRAND_LENGTH)]
    name: Annotated[str, Field(max_length=MAX_NAME_LENGTH)]
    description: Annotated[str, Field(max_length=MAX_DESCRIPTION_LENGTH)]
    skus: list[ResponseSku]

    model_config = {"from_attributes": True}
