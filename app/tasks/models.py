from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey
from app.infrastructure import Base


class Tasks(Base):
    name: Mapped[Optional[str]] = mapped_column(String(300))
    pomodoro_count: Mapped[int]
    category_id: Mapped[int]
    user_id: Mapped[int] = mapped_column(ForeignKey("userprofile.id"))


class Category(Base):
    name: Mapped[Optional[str]] = mapped_column(String(300))
    type: Mapped[Optional[str]]
