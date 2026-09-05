from backend.risk.disease_rules import DISEASE_RULES


def calculate_risk(
    disease,
    temperature,
    humidity,
    rainfall,
    rain_probability
):

    if disease not in DISEASE_RULES:
        return {"error": "Disease not supported"}

    rules = DISEASE_RULES[disease]

    score = 0
    factors = []

    # Temperature - 25 points
    min_temp, max_temp = rules["temperature"]

    if min_temp <= temperature <= max_temp:
        score += 25
        factors.append("Temperature is suitable for disease development")
    else:
        factors.append("Temperature is outside the high-risk range")

    # Humidity - 35 points
    if humidity >= rules["humidity"]:
        score += 35
        factors.append("Humidity is high")
    else:
        factors.append("Humidity is below the risk threshold")

    # Rainfall - 20 points
    if rainfall >= rules["rainfall"]:
        score += 20
        factors.append("Recent rainfall increases disease risk")
    else:
        factors.append("Rainfall is below the risk threshold")

    # Rain probability - 20 points
    if rain_probability >= rules["rain_probability"]:
        score += 20
        factors.append("High probability of rain")
    else:
        factors.append("Rain probability is low")

    # Risk level
    if score >= 70:
        risk_level = "HIGH"
    elif score >= 40:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "disease": disease,
        "risk_score": score,
        "risk_level": risk_level,
        "factors": factors
    }