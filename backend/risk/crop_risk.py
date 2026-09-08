from backend.risk.disease_rules import CROP_DISEASES
from backend.risk.risk_engine import calculate_risk


def evaluate_crop_disease_alerts(crop: str, weather_data: dict):
    crop_key = crop.lower()
    if crop_key not in CROP_DISEASES:
        return {"crop": crop, "alerts": []}

    alerts = []
    diseases = CROP_DISEASES[crop_key]

    # Current weather metrics
    temp = weather_data.get("current_temp")
    humidity = weather_data.get("current_humidity")
    rainfall = weather_data.get("current_rainfall", 0)
    rain_prob = weather_data.get("rain_probability", 0)

    for disease in diseases:
        result = calculate_risk(
            disease, temp, humidity, rainfall, rain_prob
        )

        # Include actionable alerts for HIGH and MEDIUM risk levels
        if result.get("risk_level") in ["HIGH", "MEDIUM"]:
            formatted_name = disease.replace("_", " ").title()
            alerts.append(
                {
                    "disease_code": disease,
                    "title": formatted_name,
                    "risk_level": result["risk_level"],
                    "risk_score": result["risk_score"],
                    "message": f"{result['risk_level']} Risk: {', '.join(result['factors'])}",
                }
            )

    return {
        "crop": crop,
        "active_alerts_count": len(alerts),
        "alerts": alerts,
    }