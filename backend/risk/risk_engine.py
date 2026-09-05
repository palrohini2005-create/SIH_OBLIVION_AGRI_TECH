from risk.disease_rules import DISEASE_RULES


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


def calculate_forecast_risk(disease, forecast):

    if disease not in DISEASE_RULES:
        return {"error": "Disease not supported"}

    scores = []
    max_score = 0
    max_index = 0

    for i in range(len(forecast["temperature"])):

        result = calculate_risk(
            disease,
            forecast["temperature"][i],
            forecast["humidity"][i],
            forecast["rainfall"][i],
            forecast["rain_probability"][i]
        )

        scores.append(result["risk_score"])

        if result["risk_score"] > max_score:
            max_score = result["risk_score"]
            max_index = i

    # Calculate improved risk trend
    first_score = scores[0]
    last_score = scores[-1]

    peak_index = scores.index(max_score)

    # Check whether the forecast reaches a significantly higher
    # risk level than the starting condition.
    if max_score >= first_score + 20:

        # Risk rises and later falls from the peak
        if peak_index > 0 and peak_index < len(scores) - 1:
            if last_score <= max_score - 20:
                trend = "PEAKING"
            else:
                trend = "INCREASING"

        # Peak occurs near the end of the forecast
        else:
            trend = "INCREASING"

    elif first_score >= last_score + 20:
        trend = "DECREASING"

    else:
        trend = "STABLE"

    # Risk level based on the highest forecast risk
    if max_score >= 70:
        risk_level = "HIGH"
    elif max_score >= 40:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "risk_score": max_score,
        "risk_level": risk_level,
        "forecast_time": forecast["time"][max_index],
        "trend": trend
    }