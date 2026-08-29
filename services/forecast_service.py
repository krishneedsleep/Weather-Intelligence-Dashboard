import requests

from config import OPENWEATHER_API_KEY


def get_forecast(city):
    """
    Get 5-day / 3-hour weather forecast from OpenWeatherMap.
    """

    url = "https://api.openweathermap.org/data/2.5/forecast"

    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    return response.json()


def process_forecast(data):
    """
    Convert OpenWeatherMap's 3-hour forecast
    into one forecast entry per day.
    """

    daily_data = {}

    forecast_list = data.get("list", [])

    for item in forecast_list:

        date = item["dt_txt"].split(" ")[0]

        temperature = item["main"]["temp"]

        condition = item["weather"][0]["description"]

        rain_probability = item.get(
            "pop",
            0
        )

        if date not in daily_data:

            daily_data[date] = {
                "temperatures": [],
                "condition": condition,
                "rain_probability": []
            }

        daily_data[date]["temperatures"].append(
            temperature
        )

        daily_data[date]["rain_probability"].append(
            rain_probability
        )

    processed = []

    for date, values in daily_data.items():

        temperatures = values["temperatures"]

        rain_values = values["rain_probability"]

        min_temp = round(
            min(temperatures),
            1
        )

        max_temp = round(
            max(temperatures),
            1
        )

        average_rain = round(
            max(rain_values) * 100
        )

        processed.append({
            "day": date,
            "condition": values["condition"],
            "min_temp": min_temp,
            "max_temp": max_temp,
            "rain_probability": average_rain
        })

    return processed[:5]