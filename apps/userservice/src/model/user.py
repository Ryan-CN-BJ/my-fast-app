from model.base import Base, IDMixin, TimestampMixin, DeleteMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from typing import Annotated


class User(Base, IDMixin, TimestampMixin, DeleteMixin):
    name: Mapped[Annotated[str, mapped_column(String(50), nullable=False)]]
    email: Mapped[Annotated[str, mapped_column(String(50), nullable=False)]]
    pwd: Mapped[Annotated[str, mapped_column(String(100), nullable=False)]]
