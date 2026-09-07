from datetime import datetime

from sqlalchemy import String, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class AnalysisHistory(Base):
    __tablename__ = "analysis_history"

    history_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    farmer_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    crop_id: Mapped[int] = mapped_column(
        ForeignKey("crops.crop_id"),
        nullable=False
    )

    disease_id: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("diseases.disease_id"),
        nullable=False
    )

    confidence: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    image_path: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    analysis_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )