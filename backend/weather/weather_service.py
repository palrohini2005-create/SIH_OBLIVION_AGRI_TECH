import requests


def get_weather(latitude, longitude):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,rain",
        "hourly": "precipitation_probability",
        "forecast_days": 1
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        if response.status_code != 200:
            return {
                "error": "Unable to fetch weather data"
            }

        data = response.json()

        return {
            "temperature": data["current"]["temperature_2m"],
            "humidity": data["current"]["relative_humidity_2m"],
            "rainfall": data["current"]["rain"],
            "rain_probability": data["hourly"]["precipitation_probability"][0]
        }

    except requests.RequestException:
        return {
            "error": "Weather service unavailable"
        }