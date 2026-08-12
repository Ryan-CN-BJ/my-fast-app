from apps.userservice.src.userservice.model.base import (
    Base,
    DeleteMixin,
    TimestampMixin,
    IDMixin,
)

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSONB

from typing import Annotated, TYPE_CHECKING
from decimal import Decimal

if TYPE_CHECKING:
    from apps.userservice.src.userservice.model.product import Product

MAX_SKU_CODE_LENGTH = 50
MAX_PRICE_DIGITS = 10
PRICE_DECIMAL_PLACES = 2


class Sku(Base, IDMixin, DeleteMixin, TimestampMixin):
    product_id: Mapped[
        Annotated[int, mapped_column(ForeignKey("product.id", ondelete="CASCADE"))]
    ]

    sku_code: Mapped[
        Annotated[str, mapped_column(String(MAX_SKU_CODE_LENGTH), unique=True)]
    ]
    price: Mapped[Annotated[Decimal, mapped_column(Numeric(10, 2))]]
    stock: Mapped[Annotated[int, mapped_column(default=0)]]
    attrs: Mapped[Annotated[dict, mapped_column(JSONB)]]
    image_url: Mapped[Annotated[str, mapped_column()]]

    product: Mapped["Product"] = relationship(back_populates="skus")
