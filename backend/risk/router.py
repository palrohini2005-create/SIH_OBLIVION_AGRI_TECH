from fastapi import APIRouter, HTTPException, Query
from backend.risk.risk_service import assess_crop_alerts
from backend.alerts.dashboard_alerts import(
    get_alert_summary,
    sort_alerts_by_priority
)

router = APIRouter(prefix="/api/alerts", tags=["Alerts"])


@router.get("/")
def get_crop_alerts(
    crop: str = Query(..., description="Crop name (e.g., tomato)"),
    latitude: float = Query(...),
    longitude: float = Query(...),
    farmer_name: str = Query("Farmer"),
    phone_number: str = Query("0000000000"),
):
    result = assess_crop_alerts(
        crop=crop,
        latitude=latitude,
        longitude=longitude,
        farmer_name=farmer_name,
        phone_number=phone_number,
    )

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    raw_alerts = result.get("alerts",[])
    sorted_alerts=sort_alerts_by_priority(raw_alerts)
    summary=get_alert_summary(sorted_alerts)

    return{
        "crop": crop,
        "total_alerts": len(sorted_alerts),
        "summary": summary,
        "alerts": sorted_alerts,
        "recommendations": result.get("recommendations", [])
    }