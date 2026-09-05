from fastapi import FastAPI
from backend.risk.risk_service import assess_disease_risk


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
    return assess_disease_risk(
        disease,
        latitude,
        longitude
    )