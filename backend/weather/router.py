from fastapi import APIRouter, HTTPException, Query
import requests

router = APIRouter(prefix="/api/weather", tags=["Weather"])


@router.get("/")
def get_weather(
    latitude: float = Query(..., description="Latitude of the location"),
    longitude: float = Query(..., description="Longitude of the location"),
):
    weather_url = "https://api.open-meteo.com/v1/forecast"
    geo_url = "https://nominatim.openstreetmap.org/reverse"

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,rain",
        "hourly": "precipitation_probability,temperature_2m,relative_humidity_2m,rain",
        "forecast_days": 2,
    }

    headers = {"User-Agent": "AgriguardApp/1.0"}

    try:
        # 1. Fetch Weather Data
        weather_res = requests.get(
            weather_url, params=weather_params, timeout=10
        )
        if weather_res.status_code != 200:
            raise HTTPException(
                status_code=502, detail="Unable to fetch weather data"
            )

        data = weather_res.json()

        # 2. Fetch Reverse Geocoding (City, State)
        geo_params = {
            "lat": latitude,
            "lon": longitude,
            "format": "json",
            "zoom": 10,
        }
        location_str = "Unknown Location"

        try:
            geo_res = requests.get(
                geo_url, params=geo_params, headers=headers, timeout=5
            )
            if geo_res.status_code == 200:
                geo_data = geo_res.json().get("address", {})
                city = (
                    geo_data.get("city")
                    or geo_data.get("town")
                    or geo_data.get("county")
                    or ""
                )
                state = geo_data.get("state", "")

                if city and state:
                    location_str = f"{city}, {state}"
                elif city or state:
                    location_str = city or state
        except requests.RequestException:
            pass  # Fall back to default location string on timeout/error

        rain_prob = data["hourly"]["precipitation_probability"][0]

        # Payload formatted for frontend dashboard cards
        return {
            "location": location_str,
            "temperature": f"{round(data['current']['temperature_2m'])}°C",
            "humidity": f"{round(data['current']['relative_humidity_2m'])}%",
            "rain_risk": f"{rain_prob}%",
            "rainfall": data["current"]["rain"],
            "forecast": {
                "time": data["hourly"]["time"][:24],
                "temperature": data["hourly"]["temperature_2m"][:24],
                "humidity": data["hourly"]["relative_humidity_2m"][:24],
                "rain_probability": data["hourly"][
                    "precipitation_probability"
                ][:24],
                "rainfall": data["hourly"]["rain"][:24],
            },
        }

    except requests.RequestException:
        raise HTTPException(
            status_code=503, detail="Weather service unavailable"
        )