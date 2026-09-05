from backend.recommendations.advisory_data import ADVISORY_DATA


def get_recommendation(disease, risk_level):

    if disease not in ADVISORY_DATA:
        return {
            "error": "No recommendation available for this disease"
        }

    advisory = ADVISORY_DATA[disease]

    if risk_level == "HIGH":
        message = "High risk detected. Take preventive action and monitor the crop closely."

    elif risk_level == "MEDIUM":
        message = "Moderate risk detected. Monitor the crop and follow preventive measures."

    else:
        message = "Low risk detected. Continue regular monitoring and preventive practices."

    return {
        "disease": advisory["title"],
        "risk_level": risk_level,
        "message": message,
        "prevention": advisory["prevention"],
        "monitoring": advisory["monitoring"],
        "treatment": advisory["treatment"]
    }