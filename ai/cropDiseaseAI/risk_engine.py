from crop_conditions import crop_conditions


def calculate_environment_risk(crop, temperature, humidity):

    # Check crop
    if crop not in crop_conditions:
        return {
            "risk": "UNKNOWN",
            "message": "Crop conditions not available"
        }

    conditions = crop_conditions[crop]

    score = 0

    # -----------------------------------------
    # TEMPERATURE CHECK
    # -----------------------------------------

    if conditions["min_temp"] <= temperature <= conditions["max_temp"]:
        score += 1

    # Ideal temperature
    if (
        conditions["ideal_temp_min"]
        <= temperature
        <= conditions["ideal_temp_max"]
    ):
        score += 1


    # -----------------------------------------
    # HUMIDITY CHECK
    # -----------------------------------------

    if (
        conditions["humidity_min"]
        <= humidity
        <= conditions["humidity_max"]
    ):
        score += 1


    # -----------------------------------------
    # CALCULATE RISK
    # -----------------------------------------

    if score == 3:

        risk = "HIGH"

    elif score == 2:

        risk = "MEDIUM"

    else:

        risk = "LOW"


    return {
        "crop": crop,
        "temperature": temperature,
        "humidity": humidity,
        "environment_risk": risk
    }