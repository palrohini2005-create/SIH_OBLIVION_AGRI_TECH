import csv
from datetime import datetime
from pathlib import Path

from sqlalchemy.orm import Session

import models
from app.core.config import settings
from app.core.database import Base, SessionLocal, engine

def read_csv(file_name: str) -> list[dict]:
    """Read a CSV file into a list of dicts."""
    path= Path(file_name)
    if not path.exists():
        print(f"Warning: File {file_name} not found.")
        return[]
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def parse_datetime(val: str | None) -> datetime:
    """Safely convert CSV strings to datetime objects."""
    if not val:
        return datetime.utcnow()
    try:
        return datetime.fromisoformat(val)
    except ValueError:
        try:
            return datetime.strptime(val, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return datetime.utcnow()

def seed(db: Session) -> None:
    Base.metadata.create_all(bind=engine)

    crop = read_csv("Crops.csv")
    crop_env = read_csv("crop_env.csv")
    disease = read_csv("Disease.csv")
    solution = read_csv("Solutions1.csv")
    symptoms = read_csv("symptoms.csv")
    farmer_crop = read_csv("FARMER_CROP.csv")
    farmer_user = read_csv("Farmer_dataset.csv")
    official = read_csv("Officials.csv")

    # Insert crops
    for row in crop:
        db.add(models.Crop(
            crop_id=row["crop_id"],   # primary key
            crop_name=row["crop_name"]
        ))
    db.flush()

    # Insert farmers
    for row in farmer_user:
        db.add(models.User(
            id=int(row["id"]),   # primary key
            name=row["name"],
            email=row["email"],
            phone=row["phone"],
            password=row["password"],
            role=row["role"],
            district=row["district"],
            village=row["village"],
            state=row["state"],
            created_at=parse_datetime(row.get("created_at")),
        ))

    # Insert officials
    for row in official:
        db.add(models.Official(
            id=int(row["id"]),   # primary key
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
            crop_id=int(row["crop_id"]),
            crop_name=row.get("crop_name"),
            min_temp=row.get("min_temperature"),
            max_temp=row.get("max_temperature"),
            ideal_temp=row.get("ideal_temperature"),
            humidity=row.get("humidity"),
            soil_type=row.get("soil_type"),
            soil_ph=row.get("soil_ph"),
            water_requirement=row.get("water_requirement"),
            sunlight_requirement=row.get("sunlight_requirement"),
            suitable_conditions=row.get("suitable_conditions")
        ))
    db.flush()

    for row in disease:
        db.add(models.Disease(
            disease_id=row["disease_id"],
            crop_id=int(row["crop_id"]),
            crop_name=row["crop_name"],
            disease_name=row["disease_name"],
            scientific_name=row.get("scientific_name"),
            causal_agent=row.get("causal_agent"),
            description=row.get("description")
        ))
    db.flush()

    for row in solution:
        db.add(models.Solution(
            solution_id=row["solution_id"],
            disease_id=row["disease_id"],
            disease_name=row["disease_name"],
            remedy=row["remedy"],
            treatment=row["treatment"],
            precaution=row["precaution"],
            prevention=row.get("prevention")
        ))

    for row in symptoms:
        db.add(models.Symptom(
            symptom_id=row["symptom_id"],
            disease_id=row["disease_id"],
            disease_name=row["disease_name"],
            symptom=row["symptom"]
        ))
    db.commit()
    print("Database successfully seeded from CSV files!")

if __name__ == "__main__":
    db_session = SessionLocal()
    try:
        seed(db_session)
    except Exception as e:
        db_session.rollback()
        print(f"Failed to seed database: {e}")
        raise e
    finally:
        db_session.close()