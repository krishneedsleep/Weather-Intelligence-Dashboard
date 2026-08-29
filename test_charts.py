import customtkinter as ctk

from ui.weather_charts import WeatherCharts


# =========================================================
# TEST WINDOW
# =========================================================

app = ctk.CTk()

app.title("Weather Charts Test")
app.geometry("1200x900")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# =========================================================
# CHART CONTAINER
# =========================================================

charts = WeatherCharts(app)

charts.show()


# =========================================================
# TEST DATA
# =========================================================

test_forecast = [
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
# UPDATE CHARTS
# =========================================================

charts.update_charts(
    test_forecast
)


# =========================================================
# RUN
# =========================================================

app.mainloop()