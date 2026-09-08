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
    crop_id= crop["id"]
    crop_env_id=crop_env["id"]
    disease_id=disease["id"]
    solution_id=solution["id"]
    symptom_id=symptoms["id"]

    # Insert crops
    for row in crop:
        db.add(models.Crop(
            crop_id=row["crop_id"],   # primary key
            crop_name=row["crop_name"]
        ))

    # Insert farmers
    for row in farmer_user:
        db.add(models.User(
            farmer_id=row["farmer_id"],   # primary key
            name=row["name"],
            email=row["email"],
            phone=row["phone"],
            password=row["password"],
            role=row["role"],
            district=row["district"],
            village=row["village"],
            state=row["state"],
            created_at=row["created_at"],
        ))

    # Insert officials
    for row in official:
        db.add(models.Official(
            official_id=row["official_id"],   # primary key
            name=row["name"],
            email=row["email"],
            phone=row["phone"],
            designation=row["designation"],
            department=row["department"],
            district = row["district"],
            state=row["state"]
        ))

    for row in crop_env:
        db.add(models.CropEnvironment(
            crop_env_id=row["crop_env_id"],
            crop_name=row["crop_name"],
            min_temp=row["min_temperature"],
            max_temp=row["max_temperature"],
            ideal_temp=row["ideal_temperature"],
            humidity=row["humidity"],
            soil_type=row["soil_type"],
            soil_ph=row["soil_ph"],
            water_requirement=row["water_requirement"],
            sunlight_requirement=row["sunlight_requirement"],
            suitable_conditions=row["suitable_conditions"]
        ))

    for row in disease:
        db.add(models.Disease(
            disease_id=row["disease_id"],
            crop_id=row["crop_id"],
            crop_name=row["crop_name"],
            disease_name=row["disease_name"],
            scientific_name=row["scientific_name"],
            causal_agent=row["causal_agent"],
            description=row["description"]
        ))

    for row in solution:
        db.add(models.Solution(
            solution_id=row["solution_id"],
            disease_id=row["disease_id"],
            disease_name=row["disease_name"],
            remedy=row["remedy"],
            treatment=row["treatment"],
            precaution=row["precaution"],
            prevention=row["prevention"]
        ))

    for row in symptoms:
        db.add(models.Symptom(
            symptom_id=row["symptom_id"],
            disease_id=row["disease_id"],
            disease_name=row["disease_name"],
            symptom=row["symptom"]
        ))