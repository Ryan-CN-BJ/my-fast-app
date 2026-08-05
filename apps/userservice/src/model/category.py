from model.base import Base, IDMixin, DeleteMixin, TimestampMixin

from typing import Annotated
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

MAX_NAME_LENGTH = 50
MAX_DESCRIPTION_LENGTH = 200


class Category(Base, IDMixin, DeleteMixin, TimestampMixin):
    name: Mapped[Annotated[str, mapped_column(String(MAX_NAME_LENGTH), nullable=False)]]
    description: Mapped[
        Annotated[str, mapped_column(String(MAX_DESCRIPTION_LENGTH), nullable=True)]
    ]
