from services.analytics_service import (
    calculate_forecast_statistics,
    analyze_air_quality,
    calculate_weather_score
)


# =========================================================
# TEST FORECAST DATA
# =========================================================

forecast = [
    {
        "day": "Mon",
        "min_temp": 22,
        "max_temp": 31,
        "rain_probability": 20
    },
    {
        "day": "Tue",
        "min_temp": 23,
        "max_temp": 32,
        "rain_probability": 45
    },
    {
        "day": "Wed",
        "min_temp": 21,
        "max_temp": 29,
        "rain_probability": 70
    },
    {
        "day": "Thu",
        "min_temp": 20,
        "max_temp": 28,
        "rain_probability": 80
    },
    {
        "day": "Fri",
        "min_temp": 22,
        "max_temp": 30,
        "rain_probability": 30
    }
]


# =========================================================
# TEST AIR QUALITY DATA
# =========================================================

air_quality = {
    "aqi": 2,
    "co": 250,
    "no2": 35,
    "o3": 80,
    "so2": 5,
    "pm2_5": 25,
    "pm10": 45,
    "nh3": 8
}


# =========================================================
# FORECAST ANALYSIS
# =========================================================

forecast_stats = calculate_forecast_statistics(
    forecast
)

print("\n===== FORECAST STATISTICS =====")

print(
    "Average Temperature:",
    forecast_stats["average_temperature"],
    "°C"
)

print(
    "Highest Temperature:",
    forecast_stats["highest_temperature"],
    "°C"
)

print(
    "Lowest Temperature:",
    forecast_stats["lowest_temperature"],
    "°C"
)

print(
    "Average Rain Probability:",
    forecast_stats["average_rain_probability"],
    "%"
)

print(
    "Highest Rain Probability:",
    forecast_stats["highest_rain_probability"],
    "%"
)


# =========================================================
# AIR QUALITY ANALYSIS
# =========================================================

air_stats = analyze_air_quality(
    air_quality
)

print("\n===== AIR QUALITY ANALYSIS =====")

print(
    "AQI:",
    air_stats["aqi"]
)

print(
    "AQI Status:",
    air_stats["aqi_status"]
)

print(
    "Dominant Pollutant:",
    air_stats["dominant_pollutant"]
)


# =========================================================
# WEATHER SCORE
# =========================================================

weather_score = calculate_weather_score(
    forecast_stats["average_temperature"],
    forecast_stats["average_rain_probability"],
    air_stats["aqi"]
)

print("\n===== WEATHER SCORE =====")

print(
    "Score:",
    weather_score["score"],
    "/ 100"
)

print(
    "Interpretation:",
    weather_score["interpretation"]
)