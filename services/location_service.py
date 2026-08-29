import requests

from config import OPENWEATHER_API_KEY


def get_coordinates(city):
    url = "https://api.openweathermap.org/geo/1.0/direct"

    params = {
        "q": city,
        "limit": 1,
        "appid": OPENWEATHER_API_KEY
    }

    response = requests.get(url, params=params, timeout=10)

    response.raise_for_status()

    locations = response.json()

    if not locations:
        raise ValueError(f"Could not find location: {city}")

    location = locations[0]

    return {
        "name": location.get("name"),
        "country": location.get("country"),
        "state": location.get("state"),
        "latitude": location["lat"],
        "longitude": location["lon"]
    }