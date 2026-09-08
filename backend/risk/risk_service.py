from backend.weather.weather_service import get_weather
from backend.risk.risk_engine import calculate_risk, calculate_forecast_risk
from backend.risk.disease_rules import CROP_DISEASES
from backend.recommendations.recommendation_service import get_recommendation
from backend.alerts.alert_engine import create_alert
from backend.alerts.dashboard_alerts import get_alert_summary
from backend.alerts.sms_service import send_sms_alert


def assess_disease_risk(
    disease,
    latitude,
    longitude,
    crop="Crop",
    farmer_name="Farmer",
    phone_number="0000000000"
):

    weather = get_weather(latitude, longitude)

    if "error" in weather:
        return weather

    risk = calculate_risk(
        disease,
        weather["temperature"],
        weather["humidity"],
        weather["rainfall"],
        weather["rain_probability"]
    )

    if "error" in risk:
        return risk

    forecast_risk = calculate_forecast_risk(
        disease,
        weather["forecast"]
    )

    if "error" in forecast_risk:
        return forecast_risk

    alert_risk = risk

    if forecast_risk["risk_score"] > risk["risk_score"]:
        alert_risk = {
            **risk,
            "risk_score": forecast_risk["risk_score"],
            "risk_level": forecast_risk["risk_level"]
        }

    alert = create_alert(
        crop,
        alert_risk,
        forecast_risk
    )

    alert_summary = get_alert_summary([alert])

    recommendation = get_recommendation(
        disease,
        risk["risk_level"],
        forecast_risk["risk_level"]
    )

    sms_alert = send_sms_alert(
        farmer_name,
        phone_number,
        disease,
        forecast_risk["risk_level"]
    )

    return {
        "weather": weather,
        "risk": risk,
        "forecast_risk": forecast_risk,
        "alert": alert,
        "alert_summary": alert_summary,
        "recommendation": recommendation,
        "sms_alert": sms_alert
    }


def assess_crop_alerts(
    crop,
    latitude,
    longitude,
    farmer_name="Farmer",
    phone_number="0000000000"
):

    crop_key = crop.lower().strip()

    if crop_key not in CROP_DISEASES:
        return {
            "error": f"No disease rules available for crop: {crop}"
        }

    diseases = CROP_DISEASES[crop_key]

    alerts = []
    recommendations = []
    sms_alerts = []

    for disease in diseases:

        result = assess_disease_risk(
            disease,
            latitude,
            longitude,
            crop,
            farmer_name,
            phone_number
        )

        if "error" in result:
            continue

        alerts.append(result["alert"])

        recommendations.append({
            "disease": disease,
            "recommendation": result["recommendation"]
        })

        sms_alerts.append(result["sms_alert"])

    alert_summary = get_alert_summary(alerts)

    alerts.sort(
        key=lambda alert: alert["risk_score"],
        reverse=True
    )

    return {
        "crop": crop,
        "alerts": alerts,
        "alert_summary": alert_summary,
        "recommendations": recommendations,
        "sms_alerts": sms_alerts
    }