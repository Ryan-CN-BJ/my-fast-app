from model.base import Base, DeleteMixin, IDMixin, TimestampMixin

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from typing import Annotated, TYPE_CHECKING

if TYPE_CHECKING:
    from model.sku import Sku


class Product(Base, DeleteMixin, IDMixin, TimestampMixin):
    brand: Mapped[Annotated[str, mapped_column(String(50), nullable=False)]]
    name: Mapped[Annotated[str, mapped_column(String(50), nullable=False)]]
    description: Mapped[Annotated[str, mapped_column(String(200), nullable=False)]]

    skus: Mapped[list["Sku"]] = relationship(back_populates="product")
