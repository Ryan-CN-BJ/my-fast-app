from userservice.model.base import (
    Base,
    IDMixin,
    DeleteMixin,
    TimestampMixin,
)

from typing import Annotated, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from userservice.model.association.product_category import (
    product_category,
)

if TYPE_CHECKING:
    from userservice.model.product import Product

MAX_NAME_LENGTH = 50
MAX_DESCRIPTION_LENGTH = 200


class Category(Base, IDMixin, DeleteMixin, TimestampMixin):
    name: Mapped[Annotated[str, mapped_column(String(MAX_NAME_LENGTH), nullable=False)]]
    description: Mapped[
        Annotated[str, mapped_column(String(MAX_DESCRIPTION_LENGTH), nullable=True)]
    ]
    products: Mapped[list["Product"]] = relationship(
        secondary=product_category, back_populates="cates"
    )
