from userservice.model.base import Base, IDMixin, DeleteMixin, TimestampMixin
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String

from typing import Annotated, TYPE_CHECKING

if TYPE_CHECKING:
    from userservice.model.setting import Setting


class SettingGroup(Base, IDMixin, DeleteMixin, TimestampMixin):
    key: Mapped[Annotated[str, mapped_column(String(100), unique=True)]]
    display_name: Mapped[Annotated[str, mapped_column(String(200), default="")]]
    description: Mapped[Annotated[str, mapped_column(String(200), default="")]]

    settings: Mapped[list["Setting"]] = relationship(back_populates="group")
