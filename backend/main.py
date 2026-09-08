from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.risk.risk_service import (
    assess_disease_risk,
    assess_crop_alerts
)

from backend.risk.disease_rules import (
    DISEASE_RULES,
    CROP_DISEASES
)


app = FastAPI(title="AgriTech Risk Management API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "AgriTech API is running"
    }


@app.get("/risk")
def get_risk(
    disease: str,
    latitude: float,
    longitude: float,
    crop: str = "Crop",
    farmer_name: str = "Farmer",
    phone_number: str = "0000000000"
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
        longitude,
        crop,
        farmer_name,
        phone_number
    )


@app.get("/alerts")
def get_alerts(
    disease: str,
    latitude: float,
    longitude: float,
    crop: str = "Crop",
    farmer_name: str = "Farmer",
    phone_number: str = "0000000000"
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

    result = assess_disease_risk(
        disease,
        latitude,
        longitude,
        crop,
        farmer_name,
        phone_number
    )

    if "error" in result:
        raise HTTPException(
            status_code=400,
            detail=result["error"]
        )

    return {
        "alert": result["alert"],
        "alert_summary": result["alert_summary"],
        "sms_alert": result["sms_alert"]
    }


@app.get("/crop-alerts")
def get_crop_alerts(
    crop: str,
    latitude: float,
    longitude: float,
    farmer_name: str = "Farmer",
    phone_number: str = "0000000000"
):

    crop_key = crop.lower().strip()

    if crop_key not in CROP_DISEASES:
        raise HTTPException(
            status_code=400,
            detail="Unsupported crop"
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

    result = assess_crop_alerts(
        crop,
        latitude,
        longitude,
        farmer_name,
        phone_number
    )

    if "error" in result:
        raise HTTPException(
            status_code=400,
            detail=result["error"]
        )

    return result