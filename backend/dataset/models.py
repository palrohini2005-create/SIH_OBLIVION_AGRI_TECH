from datetime import datetime

from sqlalchemy import Integer, String, Text, ForeignKey, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

#imported from crop.py
class Crop(Base):
    __tablename__ = "crops"

    crop_id: Mapped[int] = mapped_column(primary_key=True)
    crop_name: Mapped[str] = mapped_column(String(100),nullable=False)

#imported from crop_env_py
class CropEnvironment(Base):

    __tablename__ = "crop_environment"

    crop_id: Mapped[int] = mapped_column(Integer,primary_key=True)
    crop_name: Mapped[str | None] = mapped_column(String(100),nullable=True)
    min_temperature: Mapped[str | None] = mapped_column(String(50),nullable=True)
    max_temperature: Mapped[str | None] = mapped_column(String(50),nullable=True)
    ideal_temperature: Mapped[str | None] = mapped_column( String(50),nullable=True)
    humidity: Mapped[str | None] = mapped_column(String(50),nullable=True)
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

#imported from disease.py
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

#imported from solution.py
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

#imported from official.py
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

#imported from user.py
class User(Base):
    __tablename__ = "users"

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
    password: Mapped[str] = mapped_column(
        String(255)
    )
    role: Mapped[str] = mapped_column(
        String(30)
    )
    district: Mapped[str] = mapped_column(
        String(100)
    )
    village: Mapped[str] = mapped_column(
        String(100)
    )
    state: Mapped[str] = mapped_column(
        String(100)
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime
    )

#imported from analysis_history.py
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

#imported from symptom.py