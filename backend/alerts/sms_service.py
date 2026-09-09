# backend/alerts/sms_service.py


def send_sms_alert(farmer_name, phone_number, disease, risk_level):
    # Skip low-risk alerts to avoid spamming
    if risk_level in ["LOW"]:
        return {"status": "skipped", "message": "Low risk; no SMS needed"}

    message = (
        f"AgriGuard Alert: Hi {farmer_name}, {disease.replace('_', ' ')} "
        f"risk is currently {risk_level}. Please check your dashboard for actions."
    )

    # Place your Twilio / SMS API vendor code here
    print(f"📱 Sending SMS to {phone_number}: {message}")

    return {"status": "sent", "phone": phone_number, "message": message}