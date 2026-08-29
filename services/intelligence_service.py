def analyze_temperature(temperature):
    """Analyze the current temperature."""

    if temperature < 10:
        return "Cold"

    elif temperature < 20:
        return "Cool"

    elif temperature < 30:
        return "Comfortable"

    elif temperature < 35:
        return "Hot"

    else:
        return "Very Hot"


def analyze_humidity(humidity):
    """Analyze humidity level."""

    if humidity < 30:
        return "Low"

    elif humidity < 60:
        return "Comfortable"

    elif humidity < 75:
        return "High"

    else:
        return "Very High"


def analyze_wind(wind_speed):
    """Analyze wind speed in m/s."""

    if wind_speed < 3:
        return "Calm"

    elif wind_speed < 7:
        return "Moderate"

    elif wind_speed < 12:
        return "Strong"

    else:
        return "Very Strong"


def analyze_rain(rain_probability):
    """Analyze probability of rain."""

    if rain_probability < 20:
        return "Low"

    elif rain_probability < 50:
        return "Moderate"

    elif rain_probability < 75:
        return "High"

    else:
        return "Very High"


def generate_recommendation(
    temperature,
    humidity,
    wind_speed,
    rain_probability
):
    """Generate a simple weather recommendation."""

    if rain_probability >= 70:
        return "Carry an umbrella. High chance of rain."

    if wind_speed >= 12:
        return "Strong winds expected. Outdoor activities may be difficult."

    if temperature >= 35:
        return "Very hot conditions. Stay hydrated and avoid prolonged sun exposure."

    if temperature < 10:
        return "Cold conditions. Wear warm clothing."

    if humidity >= 75:
        return "High humidity. Outdoor conditions may feel uncomfortable."

    return "Weather conditions look suitable for outdoor activities."


def get_weather_intelligence(
    temperature,
    humidity,
    wind_speed,
    rain_probability
):
    """Return all weather intelligence in one dictionary."""

    return {
        "temperature_status": analyze_temperature(
            temperature
        ),

        "humidity_status": analyze_humidity(
            humidity
        ),

        "wind_status": analyze_wind(
            wind_speed
        ),

        "rain_status": analyze_rain(
            rain_probability
        ),

        "recommendation": generate_recommendation(
            temperature,
            humidity,
            wind_speed,
            rain_probability
        )
    }