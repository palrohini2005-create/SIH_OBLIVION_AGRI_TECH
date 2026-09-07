from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Disease(Base):
    __tablename__ = "diseases"

    disease_id: Mapped[str] = mapped_column(
        String(10),
        primary_key=True
    )

    crop_id: Mapped[int] = mapped_column(
        ForeignKey("crops.crop_id"),
        nullable=False
    )

    crop_name: Mapped[str] = mapped_column(
        String(100)
    )

    disease_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    scientific_name: Mapped[str] = mapped_column(
        String(200)
    )

    causal_agent: Mapped[str] = mapped_column(
        String(100)
    )

    description: Mapped[str] = mapped_column(
        Text
    )