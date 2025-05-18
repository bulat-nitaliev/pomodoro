from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from app.infrastructure import Base


class UserProfile(Base):
    username: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String(100))
