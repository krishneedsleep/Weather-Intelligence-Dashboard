from services.forecast_service import (
    get_forecast,
    process_forecast
)


city = input("Enter city name: ")

try:

    raw_data = get_forecast(city)

    forecast = process_forecast(raw_data)

    print("\n5-Day Forecast")
    print("=" * 60)

    for day in forecast:

        print(
            f"{day['day']} | "
            f"{day['min_temp']:.1f}°C - "
            f"{day['max_temp']:.1f}°C | "
            f"{day['condition'].title()} | "
            f"Rain: {day['rain_probability']:.0f}%"
        )

except Exception as error:

    print("\nSomething went wrong:")
    print(error)