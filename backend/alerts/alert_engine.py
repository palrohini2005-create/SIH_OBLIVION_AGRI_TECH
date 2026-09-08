def determine_alert_severity(risk_score):
    if risk_score >= 90:
        return "CRITICAL"
    elif risk_score >= 70:
        return "HIGH"
    elif risk_score >= 40:
        return "MEDIUM"
    else:
        return "LOW"


def create_alert(crop, risk_result, forecast_risk=None):
    if "error" in risk_result:
        return risk_result

    risk_level = risk_result["risk_level"]
    alert_severity = determine_alert_severity(risk_result["risk_score"])

    alert = {
        "crop": crop,
        "disease": risk_result["disease"],
        "risk_score": risk_result["risk_score"],
        "risk_level": risk_level,
        "alert_severity": alert_severity,
        "factors": risk_result["factors"],
        "message": (
            f"{alert_severity} alert: "
            f"{risk_result['disease'].replace('_', ' ')} "
            f"detected in {crop}."
        )
    }

    if forecast_risk:
        alert["forecast_time"] = forecast_risk["forecast_time"]
        alert["trend"] = forecast_risk["trend"]

    return alert