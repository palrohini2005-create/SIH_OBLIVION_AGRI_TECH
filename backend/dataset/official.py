from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Official(Base):
    __tablename__ = "officers"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100)
    )

    email: Mapped[str] = mapped_column(
        String(100),
        unique=True
    )

    phone: Mapped[str] = mapped_column(
        String(20)
    )

    designation: Mapped[str] = mapped_column(
        String(150)
    )

    department: Mapped[str] = mapped_column(
        String(150)
    )

    district: Mapped[str] = mapped_column(
        String(100)
    )

    state: Mapped[str] = mapped_column(
        String(100)
    )