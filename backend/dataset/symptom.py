from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Symptom(Base):
    __tablename__ = "symptoms"

    symptom_id: Mapped[str] = mapped_column(
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

    symptom: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )