from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Solution(Base):
    __tablename__ = "solutions"

    solution_id: Mapped[str] = mapped_column(
        String(10),
        primary_key=True
    )

    disease_id: Mapped[str] = mapped_column(
        String(10),
        ForeignKey("diseases.disease_id"),
        nullable=False
    )

    disease_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    remedy: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    treatment: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    precaution: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    prevention: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )