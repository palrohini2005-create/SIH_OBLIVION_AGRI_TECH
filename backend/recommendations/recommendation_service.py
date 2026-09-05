
from backend.recommendations.advisory_data import ADVISORY_DATA


def get_recommendation(disease, risk_level, forecast_risk_level=None):

    if disease not in ADVISORY_DATA:
        return {
            "error": "No recommendation available for this disease"
        }

    advisory = ADVISORY_DATA[disease]

    if risk_level == "HIGH":
        message = "High disease risk detected. Take preventive action and monitor the crop closely."

    elif forecast_risk_level == "HIGH":
        message = "High disease risk is expected in the forecast. Take preventive action before conditions worsen."

    elif risk_level == "MEDIUM":
        message = "Moderate disease risk detected. Monitor the crop and follow preventive measures."

    else:
        message = "Low disease risk detected. Continue regular monitoring and preventive practices."

    return {
        "disease": advisory["title"],
        "risk_level": risk_level,
        "forecast_risk_level": forecast_risk_level,
        "message": message,
        "prevention": advisory["prevention"],
        "monitoring": advisory["monitoring"],
        "treatment": advisory["treatment"]
    }

