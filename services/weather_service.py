import requests

from config import OPENWEATHER_API_KEY


def get_current_weather(city):
    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    response = requests.get(url, params=params, timeout=10)

    response.raise_for_status()

    return response.json()