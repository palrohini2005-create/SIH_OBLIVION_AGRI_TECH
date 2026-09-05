from fastapi import FastAPI, HTTPException
from backend.risk.risk_service import assess_disease_risk
from backend.risk.disease_rules import DISEASE_RULES


app = FastAPI(title="AgriTech Risk Management API")


@app.get("/")
def home():
    return {
        "message": "AgriTech API is running"
    }


@app.get("/risk")
def get_risk(
    disease: str,
    latitude: float,
    longitude: float
):

    if disease not in DISEASE_RULES:
        raise HTTPException(
            status_code=400,
            detail="Unsupported disease"
        )

    if not -90 <= latitude <= 90:
        raise HTTPException(
            status_code=400,
            detail="Invalid latitude"
        )

    if not -180 <= longitude <= 180:
        raise HTTPException(
            status_code=400,
            detail="Invalid longitude"
        )

    return assess_disease_risk(
        disease,
        latitude,
        longitude
    )