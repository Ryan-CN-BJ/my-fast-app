from pydantic import BaseModel, Field
from typing import Annotated
from apps.userservice.src.userservice.model.category import (
    MAX_NAME_LENGTH,
    MAX_DESCRIPTION_LENGTH,
)


class CreateCategory(BaseModel):
    name: Annotated[str, Field(max_length=MAX_NAME_LENGTH)]
    description: Annotated[str, Field(max_length=MAX_DESCRIPTION_LENGTH)]


class ResponseCategory(BaseModel):
    id: int
    name: Annotated[str, Field(max_length=MAX_NAME_LENGTH)]
    description: Annotated[str, Field(max_length=MAX_DESCRIPTION_LENGTH)]

    model_config = {"from_attributes": True}
