```python
from weather.weather_service import get_weather
from risk.risk_engine import calculate_risk, calculate_forecast_risk
from recommendations.recommendation_service import get_recommendation
from backend.alerts.sms_service import send_sms_alert


def assess_disease_risk(disease, latitude, longitude):

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

    recommendation = get_recommendation(
        disease,
        risk["risk_level"],
        forecast_risk["risk_level"]
    )

    sms_alert = send_sms_alert(
        "Farmer",
        "0000000000",
        disease,
        forecast_risk["risk_level"]
    )

    return {
        "weather": weather,
        "risk": risk,
        "forecast_risk": forecast_risk,
        "recommendation": recommendation,
        "sms_alert": sms_alert
    }
```
