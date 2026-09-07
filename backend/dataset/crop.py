from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Crop(Base):
    __tablename__ = "crops"

    crop_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    crop_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )