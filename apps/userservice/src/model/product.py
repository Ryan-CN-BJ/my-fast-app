from model.base import Base, DeleteMixin, IDMixin, TimestampMixin

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from typing import Annotated, TYPE_CHECKING

if TYPE_CHECKING:
    from model.sku import Sku


MAX_BRAND_LENGTH = 50
MAX_NAME_LENGTH = 50
MAX_DESCRIPTION_LENGTH = 200


class Product(Base, DeleteMixin, IDMixin, TimestampMixin):
    brand: Mapped[
        Annotated[str, mapped_column(String(MAX_BRAND_LENGTH), nullable=False)]
    ]
    name: Mapped[Annotated[str, mapped_column(String(MAX_NAME_LENGTH), nullable=False)]]
    description: Mapped[
        Annotated[str, mapped_column(String(MAX_DESCRIPTION_LENGTH), nullable=False)]
    ]

    skus: Mapped[list["Sku"]] = relationship(back_populates="product")
