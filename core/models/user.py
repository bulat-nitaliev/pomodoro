from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from core.database import Base


class UserProfile(Base):
    username: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String(100))