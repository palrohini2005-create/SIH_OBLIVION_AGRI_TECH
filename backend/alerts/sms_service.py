def send_sms_alert(farmer_name, phone_number, disease, risk_level):

    if risk_level != "HIGH":
        return {
            "sms_sent": False,
            "message": "SMS alert not required"
        }

    message = (
        f"AgriTech Alert: High risk of {disease.replace('_', ' ')} "
        f"is expected in your area. Please monitor your crop "
        f"and take preventive action."
    )

    return {
        "sms_sent": True,
        "recipient": farmer_name,
        "phone_number": phone_number,
        "message": message,
        "type": "DUMMY_SMS"
    }