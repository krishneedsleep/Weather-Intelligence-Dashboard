def calculate_forecast_statistics(forecast):
    """
    Calculate statistical information
    from the processed forecast data.
    """

    if not forecast:
        return {
            "average_temperature": 0,
            "highest_temperature": 0,
            "lowest_temperature": 0,
            "average_rain_probability": 0,
            "highest_rain_probability": 0
        }

    temperatures = []
    rain_probabilities = []

    for day in forecast:

        # -------------------------------------------------
        # TEMPERATURE
        # -------------------------------------------------

        min_temp = day.get("min_temp")
        max_temp = day.get("max_temp")

        if (
            isinstance(min_temp, (int, float))
            and isinstance(max_temp, (int, float))
        ):
            average_temp = (
                min_temp + max_temp
            ) / 2

            temperatures.append(
                average_temp
            )

        else:

            temperature = day.get(
                "temperature"
            )

            try:
                temperatures.append(
                    float(temperature)
                )
            except (
                ValueError,
                TypeError
            ):
                pass

        # -------------------------------------------------
        # RAIN PROBABILITY
        # -------------------------------------------------

        rain = day.get(
            "rain_probability",
            0
        )

        try:

            rain = float(rain)

            if rain <= 1:
                rain *= 100

            rain = max(
                0,
                min(
                    100,
                    rain
                )
            )

            rain_probabilities.append(
                rain
            )

        except (
            ValueError,
            TypeError
        ):
            pass

    # -----------------------------------------------------
    # CALCULATE TEMPERATURE STATISTICS
    # -----------------------------------------------------

    if temperatures:

        average_temperature = (
            sum(temperatures)
            / len(temperatures)
        )

        highest_temperature = max(
            temperatures
        )

        lowest_temperature = min(
            temperatures
        )

    else:

        average_temperature = 0
        highest_temperature = 0
        lowest_temperature = 0

    # -----------------------------------------------------
    # CALCULATE RAIN STATISTICS
    # -----------------------------------------------------

    if rain_probabilities:

        average_rain_probability = (
            sum(rain_probabilities)
            / len(rain_probabilities)
        )

        highest_rain_probability = max(
            rain_probabilities
        )

    else:

        average_rain_probability = 0
        highest_rain_probability = 0

    return {
        "average_temperature": round(
            average_temperature,
            1
        ),
        "highest_temperature": round(
            highest_temperature,
            1
        ),
        "lowest_temperature": round(
            lowest_temperature,
            1
        ),
        "average_rain_probability": round(
            average_rain_probability
        ),
        "highest_rain_probability": round(
            highest_rain_probability
        )
    }


def analyze_air_quality(air_quality):
    """
    Analyze pollutant data and determine
    the dominant pollutant.
    """

    if not air_quality:

        return {
            "aqi": 0,
            "aqi_status": "Unknown",
            "dominant_pollutant": "Unknown"
        }

    aqi = air_quality.get(
        "aqi",
        0
    )

    aqi_statuses = {
        1: "Good",
        2: "Fair",
        3: "Moderate",
        4: "Poor",
        5: "Very Poor"
    }

    aqi_status = aqi_statuses.get(
        aqi,
        "Unknown"
    )

    pollutants = {
        "PM2.5": air_quality.get(
            "pm2_5",
            0
        ),
        "PM10": air_quality.get(
            "pm10",
            0
        ),
        "CO": air_quality.get(
            "co",
            0
        ),
        "NO₂": air_quality.get(
            "no2",
            0
        ),
        "O₃": air_quality.get(
            "o3",
            0
        ),
        "SO₂": air_quality.get(
            "so2",
            0
        ),
        "NH₃": air_quality.get(
            "nh3",
            0
        )
    }

    valid_pollutants = {}

    for name, value in pollutants.items():

        try:

            valid_pollutants[name] = float(
                value
            )

        except (
            ValueError,
            TypeError
        ):
            pass

    if valid_pollutants:

        dominant_pollutant = max(
            valid_pollutants,
            key=valid_pollutants.get
        )

    else:

        dominant_pollutant = "Unknown"

    return {
        "aqi": aqi,
        "aqi_status": aqi_status,
        "dominant_pollutant": dominant_pollutant
    }


def calculate_weather_score(
    average_temperature,
    average_rain_probability,
    aqi
):
    """
    Calculate an overall weather score
    from 0 to 100.

    This is a project-specific heuristic,
    not an official meteorological score.
    """

    score = 100

    # -----------------------------------------------------
    # RAIN PENALTY
    # -----------------------------------------------------

    if average_rain_probability >= 80:

        score -= 35

    elif average_rain_probability >= 60:

        score -= 25

    elif average_rain_probability >= 40:

        score -= 15

    elif average_rain_probability >= 20:

        score -= 5

    # -----------------------------------------------------
    # AQI PENALTY
    # -----------------------------------------------------

    aqi_penalty = {
        1: 0,
        2: 5,
        3: 15,
        4: 25,
        5: 40
    }

    score -= aqi_penalty.get(
        aqi,
        0
    )

    # -----------------------------------------------------
    # TEMPERATURE PENALTY
    # -----------------------------------------------------

    if average_temperature < 5:

        score -= 20

    elif average_temperature < 10:

        score -= 10

    elif average_temperature > 40:

        score -= 25

    elif average_temperature > 35:

        score -= 15

    # -----------------------------------------------------
    # LIMIT SCORE
    # -----------------------------------------------------

    score = max(
        0,
        min(
            100,
            score
        )
    )

    # -----------------------------------------------------
    # INTERPRETATION
    # -----------------------------------------------------

    if score >= 80:

        interpretation = (
            "Excellent conditions"
        )

    elif score >= 60:

        interpretation = (
            "Good conditions"
        )

    elif score >= 40:

        interpretation = (
            "Moderate conditions"
        )

    elif score >= 20:

        interpretation = (
            "Poor conditions"
        )

    else:

        interpretation = (
            "Very poor conditions"
        )

    return {
        "score": score,
        "interpretation": interpretation
    }