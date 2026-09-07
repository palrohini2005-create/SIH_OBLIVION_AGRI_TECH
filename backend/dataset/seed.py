import csv

from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models
from app.core.config import settings
from app.core.database import Base, SessionLocal, engine

def read_csv(path: str) -> list[dict]:
    """Read a CSV file into a list of dicts."""
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def seed(db: Session) -> None:
    crop = read_csv("Crops.csv")
    crop_env = read_csv("crop_env.csv")
    disease = read_csv("Disease.csv")
    solution = read_csv("Solutions1.csv")
    symptoms = read_csv("symptoms.csv")
    farmer_crop = read_csv("FARMER_CROP.csv")
    farmer_user = read_csv("Farmer_dataset.csv")
    official = read_csv("Officials.csv")

    farmer_id =farmer_user["id"]
    official = official["id"]