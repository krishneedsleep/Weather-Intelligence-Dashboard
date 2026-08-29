import requests

from config import OPENWEATHER_API_KEY


def get_air_quality(latitude, longitude):
    url = "https://api.openweathermap.org/data/2.5/air_pollution"

    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": OPENWEATHER_API_KEY
    }

    response = requests.get(url, params=params, timeout=10)

    response.raise_for_status()

    data = response.json()

    if not data.get("list"):
        raise ValueError("No air quality data found.")

    air_data = data["list"][0]

    return {
        "aqi": int(air_data["main"]["aqi"]),
        "co": air_data["components"]["co"],
        "no2": air_data["components"]["no2"],
        "o3": air_data["components"]["o3"],
        "so2": air_data["components"]["so2"],
        "pm2_5": air_data["components"]["pm2_5"],
        "pm10": air_data["components"]["pm10"],
        "nh3": air_data["components"]["nh3"]
    }