from userservice.model.base import IDMixin, TimestampMixin, DeleteMixin, Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey
from typing import Annotated, TYPE_CHECKING

if TYPE_CHECKING:
    from userservice.model.setting_group import SettingGroup


class Setting(Base, IDMixin, TimestampMixin, DeleteMixin):
    key: Mapped[Annotated[str, mapped_column(String(50), unique=True)]]
    value: Mapped[Annotated[str, mapped_column(String(200), default="")]]
    display_name: Mapped[Annotated[str, mapped_column(String(200), default="")]]
    description: Mapped[Annotated[str, mapped_column(String(200), default="")]]

    group_id: Mapped[
        Annotated[int, mapped_column(ForeignKey("settinggroup.id", ondelete="CASCADE"))]
    ]

    group: Mapped["SettingGroup"] = relationship(back_populates="settings")
