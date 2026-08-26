from userservice.model.base import IDMixin, TimestampMixin, DeleteMixin, Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey
from typing import Annotated, TYPE_CHECKING

if TYPE_CHECKING:
    from userservice.model.setting_group import SettingGroup


class Setting(Base, IDMixin, TimestampMixin, DeleteMixin):
    key: Annotated[Mapped[str], mapped_column(String(50), unique=True)]
    value: Annotated[Mapped[str], mapped_column(String(200), default="")]
    display_name: Annotated[Mapped[str], mapped_column(String(200), default="")]
    description: Annotated[Mapped[str], mapped_column(String(200), default="")]

    group_id: Annotated[
        Mapped[int], mapped_column(ForeignKey("settingGroup.id", ondelete="CASCADE"))
    ]

    group: Mapped["SettingGroup"] = relationship(back_populates="settings")
