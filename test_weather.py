import requests

from services.weather_service import get_current_weather


city = input("Enter city name: ")

try:
    weather = get_current_weather(city)

    print("\nWeather API connected successfully!")
    print("-----------------------------------")

    print("City:", weather["name"])
    print("Country:", weather["sys"]["country"])
    print("Temperature:", weather["main"]["temp"], "°C")
    print("Feels Like:", weather["main"]["feels_like"], "°C")
    print("Humidity:", weather["main"]["humidity"], "%")
    print("Pressure:", weather["main"]["pressure"], "hPa")
    print("Wind Speed:", weather["wind"]["speed"], "m/s")
    print("Condition:", weather["weather"][0]["description"])

except requests.exceptions.HTTPError as error:
    print("API request failed:", error)

except Exception as error:
    print("Something went wrong:", error)