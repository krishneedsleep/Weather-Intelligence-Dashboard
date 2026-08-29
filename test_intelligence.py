from services.intelligence_service import get_weather_intelligence


result = get_weather_intelligence(
    temperature=28,
    humidity=55,
    wind_speed=3,
    rain_probability=20
)


print("WEATHER INTELLIGENCE")
print("--------------------")

print("Temperature:", result["temperature_status"])
print("Humidity:", result["humidity_status"])
print("Wind:", result["wind_status"])
print("Rain:", result["rain_status"])
print("Recommendation:", result["recommendation"])