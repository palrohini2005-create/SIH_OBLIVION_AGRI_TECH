from backend.weather.weather_service import get_weather
from backend.risk.risk_engine import calculate_risk


latitude = 22.5726
longitude = 88.3639

weather = get_weather(latitude, longitude)

result = calculate_risk(
    "tomato_early_blight",
    weather["temperature"],
    weather["humidity"],
    weather["rainfall"],
    weather["rain_probability"]
)

print("Weather:", weather)
print("Risk:", result)