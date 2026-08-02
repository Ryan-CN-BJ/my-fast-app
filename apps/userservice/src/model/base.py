from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy import Identity, DateTime, Boolean, func
from datetime import datetime

from typing import Annotated


class Base(DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls):
        return cls.__name__.lower()


class IDMixin:
    id: Mapped[Annotated[int, mapped_column(Identity(), primary_key=True)]]


class TimestampMixin:
    created_at: Mapped[
        Annotated[datetime, mapped_column(DateTime, server_default=func.now())]
    ]
    updated_at: Mapped[
        Annotated[
            datetime,
            mapped_column(DateTime, server_default=func.now(), onupdate=func.now()),
        ]
    ]


class DeleteMixin:
    is_deleted: Mapped[
        Annotated[bool, mapped_column(Boolean, default=False, index=True)]
    ]
    deleted_at: Mapped[
        Annotated[datetime | None, mapped_column(DateTime, nullable=True)]
    ]
