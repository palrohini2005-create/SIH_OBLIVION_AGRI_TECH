from backend.weather.weather_service import get_weather
from backend.risk.risk_engine import calculate_risk
from backend.recommendations.recommendation_service import get_recommendation


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

    recommendation = get_recommendation(
        disease,
        risk["risk_level"]
    )

    return {
        "weather": weather,
        "risk": risk,
        "recommendation": recommendation
    }