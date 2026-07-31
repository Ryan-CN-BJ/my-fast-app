from model.base import Base, IDMixin, TimestampMixin, DeleteMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class User(Base, IDMixin, TimestampMixin, DeleteMixin):
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    pwd: Mapped[str] = mapped_column(String, nullable=False)
