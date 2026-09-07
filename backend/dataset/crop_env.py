from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class CropEnvironment(Base):

    __tablename__ = "crop_environment"

    crop_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    crop_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    min_temperature: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    max_temperature: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    ideal_temperature: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    humidity: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    rainfall: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    soil_type: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True
    )

    soil_ph: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    water_requirement: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    sunlight_requirement: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    suitable_conditions: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )