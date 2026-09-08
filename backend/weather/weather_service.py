import requests


def get_weather(latitude, longitude):

    weather_url = "https://api.open-meteo.com/v1/forecast"
    geo_url="http://nominatim.openstreetmap.org.reverse"

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,rain",
        "hourly": "temperature_2m,relative_humidity_2m,precipitation_probability,rain",
        "forecast_days": 2
    }

    headers = {"User-Agent": "Agriguard/1.0"}

    try:
        #fetch weather data
        weather_res=requests.get(
            weather_url, params=weather_params, timeout=10
        )
        if weather_res.status_code !=200:
            return{"error": "Unable to fetch weather data"}

        data = weather_res.json()

        #fetch Reverse Geocoding (city,state)
        geo_params={
            "latitude": latitude,
            "longitude": longitude,
            "format": "json",
            "zoom": 10
        }
        location_str = "Unknown Location"

        try:
            geo_res=requests.get(
                geo_url, params=geo_params, headers=headers, timeout=5
            )
            if geo_res.status_code == 200:
                geo_data = geo_res.json().get("address",{})
                city = (
                    geo_data.get("city")
                    or geo_data.get("town")
                    or geo_data.get("county")
                    or ""
                )
                state= geo_data.get("state","")

                if city and state:
                    location_str=f"{city},{state}"
                elif city or state:
                    location_str = city or state
        except requests.RequestException:
            pass #Fall back to default if location lookup fails

        rain_prob = data["hours"]["precipitation_probability"][0]

        return {
            "location": location_str,
            "temperature": f"{round(data["current"]["temperature_2m"])}°C",
            "humidity": f"{round(data["current"]["relative_humidity_2m"])}%",
            "rainfall": data["current"]["rain"],
            "rain_risk": data["current"]["rain"],
            "forecast": {
                "time": data["hourly"]["time"][:24],
                "temperature": data["hourly"]["temperature_2m"][:24],
                "humidity": data["hourly"]["relative_humidity_2m"][:24],
                "rain_probability": data["hourly"]["precipitation_probability"][:24],
                "rainfall": data["hourly"]["rain"][:24]
            }
        }

    except requests.RequestException:
        return {
            "error": "Weather service unavailable"
        }