import requests
import customtkinter as ctk
from datetime import datetime

from services.weather_service import get_current_weather
from services.forecast_service import get_forecast, process_forecast
from services.intelligence_service import get_weather_intelligence
from services.air_quality_service import get_air_quality
from services.location_service import get_coordinates
from services.analytics_service import (
    calculate_forecast_statistics,
    analyze_air_quality,
    calculate_weather_score,
)
from ui.weather_charts import WeatherCharts

try:
    from ui.weather_visuals import WeatherVisuals
except ImportError:
    WeatherVisuals = None


class WeatherDashboard(ctk.CTk):

    def __init__(self):
        super().__init__()

        # =====================================================
        # WINDOW
        # =====================================================

        self.title("Weather Intelligence Dashboard")
        self.geometry("1200x900")
        self.minsize(1000, 650)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # =====================================================
        # COLORS
        # =====================================================

        self.bg_color = "#0B1220"
        self.card_color = "#17232E"
        self.card_color_2 = "#1E2F3D"
        self.hover_color = "#294052"

        self.text_color = "#FFFFFF"
        self.secondary_text = "#AAB4BE"
        self.accent_color = "#4DA6FF"

        self.success_color = "#65D685"
        self.warning_color = "#F5B942"
        self.error_color = "#FF6B6B"

        self.configure(
            fg_color=self.bg_color
        )

        # =====================================================
        # DATA
        # =====================================================

        self.current_weather = None
        self.current_city = ""
        self.forecast_data = None
        self.air_quality_data = None

        self.forecast_cards = []
        self.selected_forecast_index = None
        self.search_history = []
        self._after_callbacks = []

        # =====================================================
        # ANIMATION STATE
        # =====================================================

        self._loading_active = False
        self._loading_step = 0
        self._pulse_step = 0

        # =====================================================
        # WEATHER VISUALS
        # =====================================================

        if WeatherVisuals:
            self.weather_visuals = WeatherVisuals(
                self
            )
        else:
            self.weather_visuals = None

        # =====================================================
        # SCROLLABLE FRAME
        # =====================================================

        self.scrollable_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=self.bg_color,
            scrollbar_button_color="#2D4050",
            scrollbar_button_hover_color="#3D5668"
        )

        self.scrollable_frame.pack(
            fill="both",
            expand=True
        )

        # =====================================================
        # BUILD UI
        # =====================================================

        self.create_header()
        self.create_search_section()
        self.create_current_weather_section()
        self.create_forecast_section()
        self.create_intelligence_section()
        self.create_air_quality_section()
        self.create_analytics_summary_section()

        # =====================================================
        # CHARTS
        # =====================================================

        self.charts = WeatherCharts(
            self.scrollable_frame
        )

        self.charts.show()

        # =====================================================
        # PROJECT FOOTER
        # =====================================================

        self.footer_label = ctk.CTkLabel(
            self.scrollable_frame,
            text=(
                "Weather Intelligence Dashboard  •  "
                "Live API Data  •  CSS241 Mini Project"
            ),
            font=("Arial", 11),
            text_color=self.secondary_text
        )

        self.footer_label.pack(
            pady=(10, 30)
        )

        # =====================================================
        # START ANIMATION
        # =====================================================

        self.animate_temperature_pulse()

        self.protocol(
            "WM_DELETE_WINDOW",
            self.close_dashboard
        )

    # =========================================================
    # CLOSE DASHBOARD
    # =========================================================

    def close_dashboard(self):

        self.stop_loading_animation()

        try:
            self.destroy()
        except Exception:
            pass

    # =========================================================
    # HEADER
    # =========================================================

    def create_header(self):

        frame = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color="transparent"
        )

        frame.pack(
            fill="x",
            padx=60,
            pady=(28, 8)
        )

        top = ctk.CTkFrame(
            frame,
            fg_color="transparent"
        )

        top.pack(
            fill="x"
        )

        self.title_label = ctk.CTkLabel(
            top,
            text="WEATHER INTELLIGENCE",
            font=("Arial", 32, "bold"),
            text_color=self.text_color
        )

        self.title_label.pack(
            side="left"
        )

        self.live_label = ctk.CTkLabel(
            top,
            text="● LIVE",
            font=("Arial", 12, "bold"),
            text_color=self.success_color
        )

        self.live_label.pack(
            side="right",
            pady=(8, 0)
        )

        self.subtitle_label = ctk.CTkLabel(
            frame,
            text=(
                "Real-time weather • Forecast • "
                "Air Quality • Analytics"
            ),
            font=("Arial", 14),
            text_color=self.secondary_text
        )

        self.subtitle_label.pack(
            anchor="w",
            pady=(6, 0)
        )

    # =========================================================
    # SEARCH SECTION
    # =========================================================

    def create_search_section(self):

        frame = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color=self.card_color,
            corner_radius=15
        )

        frame.pack(
            fill="x",
            padx=60,
            pady=15
        )

        # -----------------------------------------------------
        # CITY ENTRY
        # -----------------------------------------------------

        self.city_entry = ctk.CTkEntry(
            frame,
            placeholder_text="Enter city name...",
            height=46,
            font=("Arial", 14)
        )

        self.city_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(20, 10),
            pady=20
        )

        # -----------------------------------------------------
        # SEARCH BUTTON
        # -----------------------------------------------------

        self.search_button = ctk.CTkButton(
            frame,
            text="SEARCH WEATHER",
            width=175,
            height=46,
            font=("Arial", 12, "bold"),
            command=self.search_weather
        )

        self.search_button.pack(
            side="right",
            padx=8,
            pady=20
        )

        # -----------------------------------------------------
        # USE MY LOCATION BUTTON
        # -----------------------------------------------------


        # -----------------------------------------------------
        # REFRESH BUTTON
        # -----------------------------------------------------

        self.refresh_button = ctk.CTkButton(
            frame,
            text="REFRESH",
            width=105,
            height=46,
            font=("Arial", 12, "bold"),
            command=self.refresh_weather,
            state="disabled"
        )

        self.refresh_button.pack(
            side="right",
            padx=(0, 20),
            pady=20
        )

        # -----------------------------------------------------
        # CLEAR BUTTON
        # -----------------------------------------------------

        self.clear_button = ctk.CTkButton(
            frame,
            text="CLEAR",
            width=80,
            height=46,
            font=("Arial", 11, "bold"),
            fg_color="#344454",
            hover_color="#43586B",
            command=self.clear_dashboard
        )

        self.clear_button.pack(
            side="right",
            padx=(0, 8),
            pady=20
        )

        # -----------------------------------------------------
        # CURRENT LOCATION
        # -----------------------------------------------------

        self.current_location_label = ctk.CTkLabel(
            frame,
            text="Current location: --",
            font=("Arial", 12),
            text_color=self.secondary_text
        )

        self.current_location_label.pack(
            side="left",
            padx=(10, 0)
        )

        # -----------------------------------------------------
        # STATUS
        # -----------------------------------------------------

        self.status_label = ctk.CTkLabel(
            frame,
            text="Enter a city to get weather information",
            font=("Arial", 12),
            text_color=self.secondary_text
        )

        self.status_label.pack(
            side="left",
            padx=10
        )

        # -----------------------------------------------------
        # ENTER KEY
        # -----------------------------------------------------

        self.city_entry.bind(
            "<Return>",
            lambda event: self.search_weather()
        )

        self.history_combo = ctk.CTkComboBox(
            frame,
            values=["Recent searches"],
            width=150,
            height=34,
            state="readonly",
            command=self.select_history_city
        )

        self.history_combo.set(
            "Recent searches"
        )

        self.history_combo.pack(
            side="right",
            padx=(0, 8),
            pady=20
        )

    # =========================================================
    # CURRENT WEATHER SECTION
    # =========================================================

    def create_current_weather_section(self):

        self.weather_frame = ctk.CTkFrame(
            self.scrollable_frame,
            corner_radius=15,
            fg_color=self.card_color
        )

        self.weather_frame.pack(
            fill="x",
            padx=60,
            pady=15
        )

        self.weather_title = ctk.CTkLabel(
            self.weather_frame,
            text="CURRENT WEATHER",
            font=("Arial", 20, "bold"),
            text_color=self.text_color
        )

        self.weather_title.pack(
            anchor="w",
            padx=25,
            pady=(20, 10)
        )

        self.weather_content = ctk.CTkFrame(
            self.weather_frame,
            fg_color="transparent"
        )

        self.weather_content.pack(
            fill="x",
            padx=25,
            pady=(0, 25)
        )

        # -----------------------------------------------------
        # CITY
        # -----------------------------------------------------

        self.city_label = ctk.CTkLabel(
            self.weather_content,
            text="--",
            font=("Arial", 28, "bold"),
            text_color=self.text_color
        )

        self.city_label.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            padx=15,
            pady=(10, 10)
        )

        # -----------------------------------------------------
        # CURRENT WEATHER ICON
        # -----------------------------------------------------

        self.current_weather_icon = ctk.CTkLabel(
            self.weather_content,
            text="☁",
            width=82,
            height=82,
            font=("Arial", 44)
        )

        self.current_weather_icon.grid(
            row=0,
            column=2,
            rowspan=2,
            padx=(35, 15),
            pady=5,
            sticky="e"
        )

        # -----------------------------------------------------
        # TEMPERATURE
        # -----------------------------------------------------

        self.temperature_label = ctk.CTkLabel(
            self.weather_content,
            text="-- °C",
            font=("Arial", 44, "bold"),
            text_color=self.accent_color
        )

        self.temperature_label.grid(
            row=1,
            column=0,
            rowspan=2,
            sticky="w",
            padx=15
        )

        # -----------------------------------------------------
        # CONDITION
        # -----------------------------------------------------

        self.condition_label = ctk.CTkLabel(
            self.weather_content,
            text="Condition: --",
            font=("Arial", 16),
            text_color=self.secondary_text
        )

        self.condition_label.grid(
            row=1,
            column=1,
            sticky="w",
            padx=30,
            pady=5
        )

        # -----------------------------------------------------
        # FEELS LIKE
        # -----------------------------------------------------

        self.feels_label = ctk.CTkLabel(
            self.weather_content,
            text="Feels Like: -- °C",
            font=("Arial", 14),
            text_color=self.secondary_text
        )

        self.feels_label.grid(
            row=2,
            column=1,
            sticky="w",
            padx=30,
            pady=5
        )

        # -----------------------------------------------------
        # HUMIDITY
        # -----------------------------------------------------

        self.humidity_label = ctk.CTkLabel(
            self.weather_content,
            text="Humidity: --%",
            font=("Arial", 14),
            text_color=self.secondary_text
        )

        self.humidity_label.grid(
            row=3,
            column=0,
            sticky="w",
            padx=15,
            pady=(20, 5)
        )

        # -----------------------------------------------------
        # PRESSURE
        # -----------------------------------------------------

        self.pressure_label = ctk.CTkLabel(
            self.weather_content,
            text="Pressure: -- hPa",
            font=("Arial", 14),
            text_color=self.secondary_text
        )

        self.pressure_label.grid(
            row=3,
            column=1,
            sticky="w",
            padx=30,
            pady=(20, 5)
        )

        # -----------------------------------------------------
        # WIND
        # -----------------------------------------------------

        self.wind_label = ctk.CTkLabel(
            self.weather_content,
            text="Wind Speed: -- m/s",
            font=("Arial", 14),
            text_color=self.secondary_text
        )

        self.wind_label.grid(
            row=4,
            column=0,
            sticky="w",
            padx=15,
            pady=5
        )

        # -----------------------------------------------------
        # COUNTRY
        # -----------------------------------------------------

        self.country_label = ctk.CTkLabel(
            self.weather_content,
            text="Country: --",
            font=("Arial", 14),
            text_color=self.secondary_text
        )

        self.country_label.grid(
            row=4,
            column=1,
            sticky="w",
            padx=30,
            pady=5
        )

        # -----------------------------------------------------
        # LAST UPDATED
        # -----------------------------------------------------

        self.updated_label = ctk.CTkLabel(
            self.weather_content,
            text="Last updated: --",
            font=("Arial", 11),
            text_color=self.secondary_text
        )

        self.updated_label.grid(
            row=5,
            column=0,
            columnspan=3,
            sticky="w",
            padx=15,
            pady=(12, 0)
        )

    # =========================================================
    # 5-DAY FORECAST
    # =========================================================

    def create_forecast_section(self):

        self.forecast_frame = ctk.CTkFrame(
            self.scrollable_frame,
            corner_radius=15,
            fg_color=self.card_color
        )

        self.forecast_frame.pack(
            fill="x",
            padx=60,
            pady=15
        )

        self.forecast_title = ctk.CTkLabel(
            self.forecast_frame,
            text="5-DAY FORECAST",
            font=("Arial", 20, "bold"),
            text_color=self.text_color
        )

        self.forecast_title.pack(
            anchor="w",
            padx=25,
            pady=(20, 10)
        )

        self.forecast_cards_frame = ctk.CTkFrame(
            self.forecast_frame,
            fg_color="transparent"
        )

        self.forecast_cards_frame.pack(
            fill="x",
            padx=15,
            pady=(0, 20)
        )

        # -----------------------------------------------------
        # SELECTED FORECAST DETAIL PANEL
        # -----------------------------------------------------

        self.forecast_detail_frame = ctk.CTkFrame(
            self.forecast_frame,
            corner_radius=12,
            fg_color=self.card_color_2
        )

        self.forecast_detail_frame.pack(
            fill="x",
            padx=25,
            pady=(0, 20)
        )

        self.forecast_detail_title = ctk.CTkLabel(
            self.forecast_detail_frame,
            text="SELECTED FORECAST",
            font=("Arial", 13, "bold"),
            text_color=self.secondary_text
        )

        self.forecast_detail_title.pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        self.forecast_detail_day = ctk.CTkLabel(
            self.forecast_detail_frame,
            text="Click a forecast card to view details.",
            font=("Arial", 20, "bold"),
            text_color=self.text_color
        )

        self.forecast_detail_day.pack(
            anchor="w",
            padx=20,
            pady=5
        )

        self.forecast_detail_condition = ctk.CTkLabel(
            self.forecast_detail_frame,
            text="",
            font=("Arial", 14),
            text_color=self.secondary_text
        )

        self.forecast_detail_condition.pack(
            anchor="w",
            padx=20,
            pady=3
        )

        self.forecast_detail_temperature = ctk.CTkLabel(
            self.forecast_detail_frame,
            text="",
            font=("Arial", 14),
            text_color=self.text_color
        )

        self.forecast_detail_temperature.pack(
            anchor="w",
            padx=20,
            pady=3
        )

        self.forecast_detail_rain = ctk.CTkLabel(
            self.forecast_detail_frame,
            text="",
            font=("Arial", 14),
            text_color=self.text_color
        )

        self.forecast_detail_rain.pack(
            anchor="w",
            padx=20,
            pady=3
        )

        self.forecast_detail_analysis = ctk.CTkLabel(
            self.forecast_detail_frame,
            text="",
            font=("Arial", 13),
            text_color=self.secondary_text,
            wraplength=1000,
            justify="left"
        )

        self.forecast_detail_analysis.pack(
            anchor="w",
            padx=20,
            pady=(7, 15)
        )

        for i in range(5):

            card = ctk.CTkFrame(
                self.forecast_cards_frame,
                corner_radius=12,
                fg_color=self.card_color_2,
                height=210
            )

            card.grid(
                row=0,
                column=i,
                padx=8,
                pady=10,
                sticky="nsew"
            )

            self.forecast_cards_frame.grid_columnconfigure(
                i,
                weight=1
            )

            # -------------------------------------------------
            # DAY
            # -------------------------------------------------

            day_label = ctk.CTkLabel(
                card,
                text="--",
                font=("Arial", 15, "bold"),
                text_color=self.text_color
            )

            day_label.pack(
                pady=(15, 5)
            )

            # -------------------------------------------------
            # ICON
            # -------------------------------------------------

            icon_label = ctk.CTkLabel(
                card,
                text="☁",
                width=56,
                height=56,
                font=("Arial", 30)
            )

            icon_label.pack(
                pady=3
            )

            # -------------------------------------------------
            # CONDITION
            # -------------------------------------------------

            condition_label = ctk.CTkLabel(
                card,
                text="--",
                font=("Arial", 12),
                text_color=self.secondary_text,
                wraplength=150
            )

            condition_label.pack(
                pady=4
            )

            # -------------------------------------------------
            # TEMPERATURE
            # -------------------------------------------------

            temperature_label = ctk.CTkLabel(
                card,
                text="-- / -- °C",
                font=("Arial", 18, "bold"),
                text_color=self.accent_color
            )

            temperature_label.pack(
                pady=4
            )

            # -------------------------------------------------
            # RAIN
            # -------------------------------------------------

            rain_label = ctk.CTkLabel(
                card,
                text="Rain: --%",
                font=("Arial", 11),
                text_color=self.secondary_text
            )

            rain_label.pack(
                pady=(5, 15)
            )

            self.forecast_cards.append({
                "card": card,
                "day": day_label,
                "icon": icon_label,
                "condition": condition_label,
                "temperature": temperature_label,
                "rain": rain_label
            })

            self.bind_card_hover(card)
            self.bind_forecast_card_click(
                card,
                i
            )

    # =========================================================
    # WEATHER INTELLIGENCE
    # =========================================================

    def create_intelligence_section(self):

        self.intelligence_frame = ctk.CTkFrame(
            self.scrollable_frame,
            corner_radius=15,
            fg_color=self.card_color
        )

        self.intelligence_frame.pack(
            fill="x",
            padx=60,
            pady=15
        )

        self.intelligence_title = ctk.CTkLabel(
            self.intelligence_frame,
            text="WEATHER INTELLIGENCE",
            font=("Arial", 20, "bold"),
            text_color=self.text_color
        )

        self.intelligence_title.pack(
            anchor="w",
            padx=25,
            pady=(20, 15)
        )

        cards_frame = ctk.CTkFrame(
            self.intelligence_frame,
            fg_color="transparent"
        )

        cards_frame.pack(
            fill="x",
            padx=15,
            pady=5
        )

        self.temperature_status = (
            self.create_intelligence_card(
                cards_frame,
                "TEMPERATURE",
                "Waiting..."
            )
        )

        self.temperature_status.grid(
            row=0,
            column=0,
            padx=8,
            pady=10,
            sticky="nsew"
        )

        self.humidity_status = (
            self.create_intelligence_card(
                cards_frame,
                "HUMIDITY",
                "Waiting..."
            )
        )

        self.humidity_status.grid(
            row=0,
            column=1,
            padx=8,
            pady=10,
            sticky="nsew"
        )

        self.wind_status = (
            self.create_intelligence_card(
                cards_frame,
                "WIND",
                "Waiting..."
            )
        )

        self.wind_status.grid(
            row=0,
            column=2,
            padx=8,
            pady=10,
            sticky="nsew"
        )

        self.rain_status = (
            self.create_intelligence_card(
                cards_frame,
                "RAIN RISK",
                "Waiting..."
            )
        )

        self.rain_status.grid(
            row=0,
            column=3,
            padx=8,
            pady=10,
            sticky="nsew"
        )

        for i in range(4):

            cards_frame.grid_columnconfigure(
                i,
                weight=1
            )

        self.bind_card_hover(
            self.temperature_status
        )

        self.bind_card_hover(
            self.humidity_status
        )

        self.bind_card_hover(
            self.wind_status
        )

        self.bind_card_hover(
            self.rain_status
        )

        self.recommendation_label = ctk.CTkLabel(
            self.intelligence_frame,
            text=(
                "Recommendation: Search for a city "
                "to get weather intelligence."
            ),
            font=("Arial", 13),
            text_color=self.secondary_text,
            wraplength=1000,
            justify="left"
        )

        self.recommendation_label.pack(
            anchor="w",
            padx=30,
            pady=(15, 25)
        )

    # =========================================================
    # AIR QUALITY
    # =========================================================

    def create_air_quality_section(self):

        self.air_quality_frame = ctk.CTkFrame(
            self.scrollable_frame,
            corner_radius=15,
            fg_color=self.card_color
        )

        self.air_quality_frame.pack(
            fill="x",
            padx=60,
            pady=15
        )

        self.air_quality_title = ctk.CTkLabel(
            self.air_quality_frame,
            text="AIR QUALITY",
            font=("Arial", 20, "bold"),
            text_color=self.text_color
        )

        self.air_quality_title.pack(
            anchor="w",
            padx=25,
            pady=(20, 15)
        )

        self.aqi_summary_frame = ctk.CTkFrame(
            self.air_quality_frame,
            corner_radius=12,
            fg_color=self.card_color_2
        )

        self.aqi_summary_frame.pack(
            fill="x",
            padx=25,
            pady=10
        )

        self.aqi_label = ctk.CTkLabel(
            self.aqi_summary_frame,
            text="AQI: --",
            font=("Arial", 28, "bold"),
            text_color=self.accent_color
        )

        self.aqi_label.pack(
            pady=(18, 3)
        )

        self.aqi_status_label = ctk.CTkLabel(
            self.aqi_summary_frame,
            text="Status: Waiting...",
            font=("Arial", 16, "bold"),
            text_color=self.text_color
        )

        self.aqi_status_label.pack(
            pady=(0, 18)
        )

        self.pollutants_frame = ctk.CTkFrame(
            self.air_quality_frame,
            fg_color="transparent"
        )

        self.pollutants_frame.pack(
            fill="x",
            padx=15,
            pady=10
        )

        pollutants = [
            ("PM2.5", "pm2_5"),
            ("PM10", "pm10"),
            ("CO", "co"),
            ("NO₂", "no2"),
            ("O₃", "o3"),
            ("SO₂", "so2"),
            ("NH₃", "nh3")
        ]

        self.pollutant_labels = {}

        for i, (name, key) in enumerate(
            pollutants
        ):

            card = ctk.CTkFrame(
                self.pollutants_frame,
                corner_radius=12,
                fg_color=self.card_color_2
            )

            card.grid(
                row=0,
                column=i,
                padx=5,
                pady=10,
                sticky="nsew"
            )

            self.pollutants_frame.grid_columnconfigure(
                i,
                weight=1
            )

            ctk.CTkLabel(
                card,
                text=name,
                font=("Arial", 11, "bold"),
                text_color=self.secondary_text
            ).pack(
                pady=(12, 3)
            )

            value_label = ctk.CTkLabel(
                card,
                text="--",
                font=("Arial", 14, "bold"),
                text_color=self.text_color
            )

            value_label.pack(
                pady=(0, 12)
            )

            self.pollutant_labels[
                key
            ] = value_label

            self.bind_card_hover(
                card
            )

    # =========================================================
    # ANALYTICS SUMMARY
    # =========================================================

    def create_analytics_summary_section(self):

        self.analytics_frame = ctk.CTkFrame(
            self.scrollable_frame,
            corner_radius=15,
            fg_color=self.card_color
        )

        self.analytics_frame.pack(
            fill="x",
            padx=60,
            pady=15
        )

        ctk.CTkLabel(
            self.analytics_frame,
            text="ANALYTICS SUMMARY",
            font=("Arial", 20, "bold"),
            text_color=self.text_color
        ).pack(
            anchor="w",
            padx=25,
            pady=(20, 15)
        )

        stats_frame = ctk.CTkFrame(
            self.analytics_frame,
            fg_color="transparent"
        )

        stats_frame.pack(
            fill="x",
            padx=25
        )

        self.average_temp_label = ctk.CTkLabel(
            stats_frame,
            text="Average Temperature: --",
            font=("Arial", 14),
            text_color=self.text_color
        )

        self.average_temp_label.grid(
            row=0,
            column=0,
            padx=10,
            pady=7,
            sticky="w"
        )

        self.highest_temp_label = ctk.CTkLabel(
            stats_frame,
            text="Highest Temperature: --",
            font=("Arial", 14),
            text_color=self.text_color
        )

        self.highest_temp_label.grid(
            row=0,
            column=1,
            padx=10,
            pady=7,
            sticky="w"
        )

        self.lowest_temp_label = ctk.CTkLabel(
            stats_frame,
            text="Lowest Temperature: --",
            font=("Arial", 14),
            text_color=self.text_color
        )

        self.lowest_temp_label.grid(
            row=1,
            column=0,
            padx=10,
            pady=7,
            sticky="w"
        )

        self.average_rain_label = ctk.CTkLabel(
            stats_frame,
            text="Average Rain Probability: --",
            font=("Arial", 14),
            text_color=self.text_color
        )

        self.average_rain_label.grid(
            row=1,
            column=1,
            padx=10,
            pady=7,
            sticky="w"
        )

        self.highest_rain_label = ctk.CTkLabel(
            stats_frame,
            text="Highest Rain Probability: --",
            font=("Arial", 14),
            text_color=self.text_color
        )

        self.highest_rain_label.grid(
            row=2,
            column=0,
            padx=10,
            pady=7,
            sticky="w"
        )

        self.aqi_summary_label = ctk.CTkLabel(
            self.analytics_frame,
            text="AQI: --",
            font=("Arial", 14),
            text_color=self.text_color
        )

        self.aqi_summary_label.pack(
            anchor="w",
            padx=35,
            pady=(14, 4)
        )

        self.dominant_pollutant_label = ctk.CTkLabel(
            self.analytics_frame,
            text="Dominant Pollutant: --",
            font=("Arial", 14),
            text_color=self.text_color
        )

        self.dominant_pollutant_label.pack(
            anchor="w",
            padx=35,
            pady=4
        )

        # -----------------------------------------------------
        # WEATHER SCORE CARD
        # -----------------------------------------------------

        self.weather_score_card = ctk.CTkFrame(
            self.analytics_frame,
            corner_radius=15,
            fg_color=self.card_color_2
        )

        self.weather_score_card.pack(
            fill="x",
            padx=25,
            pady=(20, 15)
        )

        ctk.CTkLabel(
            self.weather_score_card,
            text="OVERALL WEATHER SCORE",
            font=("Arial", 12, "bold"),
            text_color=self.secondary_text
        ).pack(
            pady=(15, 0)
        )

        self.weather_score_label = ctk.CTkLabel(
            self.weather_score_card,
            text="-- / 100",
            font=("Arial", 38, "bold"),
            text_color=self.accent_color
        )

        self.weather_score_label.pack(
            pady=4
        )

        self.weather_score_progress = ctk.CTkProgressBar(
            self.weather_score_card,
            height=12,
            corner_radius=8,
            progress_color=self.accent_color,
            fg_color="#0F1B27"
        )

        self.weather_score_progress.set(
            0
        )

        self.weather_score_progress.pack(
            fill="x",
            padx=40,
            pady=(4, 10)
        )

        self.weather_score_interpretation = ctk.CTkLabel(
            self.weather_score_card,
            text="Waiting for weather data...",
            font=("Arial", 15, "bold"),
            text_color=self.secondary_text
        )

        self.weather_score_interpretation.pack(
            pady=(0, 12)
        )

        factor_frame = ctk.CTkFrame(
            self.weather_score_card,
            fg_color="transparent"
        )

        factor_frame.pack(
            fill="x",
            padx=35,
            pady=(0, 15)
        )

        self.score_temperature_factor = ctk.CTkLabel(
            factor_frame,
            text="Temperature: Waiting...",
            font=("Arial", 12),
            text_color=self.secondary_text
        )

        self.score_temperature_factor.grid(
            row=0,
            column=0,
            padx=10,
            pady=5,
            sticky="w"
        )

        self.score_rain_factor = ctk.CTkLabel(
            factor_frame,
            text="Rain: Waiting...",
            font=("Arial", 12),
            text_color=self.secondary_text
        )

        self.score_rain_factor.grid(
            row=0,
            column=1,
            padx=10,
            pady=5,
            sticky="w"
        )

        self.score_aqi_factor = ctk.CTkLabel(
            factor_frame,
            text="Air Quality: Waiting...",
            font=("Arial", 12),
            text_color=self.secondary_text
        )

        self.score_aqi_factor.grid(
            row=1,
            column=0,
            padx=10,
            pady=5,
            sticky="w"
        )

        self.score_pollutant_factor = ctk.CTkLabel(
            factor_frame,
            text="Dominant Pollutant: Waiting...",
            font=("Arial", 12),
            text_color=self.secondary_text
        )

        self.score_pollutant_factor.grid(
            row=1,
            column=1,
            padx=10,
            pady=5,
            sticky="w"
        )

        factor_frame.grid_columnconfigure(
            0,
            weight=1
        )

        factor_frame.grid_columnconfigure(
            1,
            weight=1
        )

        self.bind_card_hover(
            self.weather_score_card
        )

    # =========================================================
    # INTELLIGENCE CARD CREATOR
    # =========================================================

    def create_intelligence_card(
        self,
        parent,
        title,
        value
    ):

        card = ctk.CTkFrame(
            parent,
            corner_radius=12,
            fg_color=self.card_color_2,
            height=100
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 11, "bold"),
            text_color=self.secondary_text
        ).pack(
            pady=(15, 5)
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Arial", 16, "bold"),
            text_color=self.text_color
        )

        value_label.pack(
            pady=(0, 15)
        )

        card.value_label = value_label

        return card

    # =========================================================
    # FORECAST CARD CLICK
    # =========================================================

    def bind_forecast_card_click(
        self,
        card,
        index
    ):
        def on_click(event):
            self.select_forecast(
                index
            )

        card.bind(
            "<Button-1>",
            on_click
        )

        for child in card.winfo_children():
            try:
                child.bind(
                    "<Button-1>",
                    on_click
                )
            except Exception:
                pass

    def select_forecast(
        self,
        index
    ):

        if not self.forecast_data:
            return

        if index < 0 or index >= len(
            self.forecast_data
        ):
            return

        self.selected_forecast_index = index

        selected = self.forecast_data[
            index
        ]

        # Highlight selected card.
        for i, card_data in enumerate(
            self.forecast_cards
        ):

            try:
                if i == index:
                    card_data["card"].configure(
                        fg_color=self.accent_color
                    )
                else:
                    card_data["card"].configure(
                        fg_color=self.card_color_2
                    )
            except Exception:
                pass

        day = selected.get(
            "day",
            "--"
        )

        condition = selected.get(
            "condition",
            "--"
        )

        minimum = selected.get(
            "min_temp",
            "--"
        )

        maximum = selected.get(
            "max_temp",
            "--"
        )

        rain = selected.get(
            "rain_probability",
            0
        )

        try:
            rain = float(rain)
            if rain <= 1:
                rain *= 100
            rain = round(
                max(
                    0,
                    min(
                        100,
                        rain
                    )
                )
            )
        except (
            ValueError,
            TypeError
        ):
            rain = 0

        # Temperature text.
        if (
            isinstance(
                minimum,
                (int, float)
            )
            and
            isinstance(
                maximum,
                (int, float)
            )
        ):
            temperature_text = (
                f"Temperature: "
                f"{minimum:.1f}°C - "
                f"{maximum:.1f}°C"
            )
        else:
            temperature = selected.get(
                "temperature",
                "--"
            )
            temperature_text = (
                f"Temperature: "
                f"{temperature}°C"
            )

        # Simple explanation based on precipitation risk.
        if rain >= 75:
            analysis = (
                "Very high precipitation risk. "
                "Carrying an umbrella and planning "
                "indoor alternatives is recommended."
            )
        elif rain >= 50:
            analysis = (
                "High precipitation risk. "
                "Outdoor activities may be affected."
            )
        elif rain >= 25:
            analysis = (
                "Moderate precipitation risk. "
                "Keep an eye on changing conditions."
            )
        else:
            analysis = (
                "Low precipitation risk. "
                "Conditions are relatively favorable "
                "for outdoor activities."
            )

        self.forecast_detail_day.configure(
            text=str(day)
        )

        self.forecast_detail_condition.configure(
            text=(
                f"Weather: "
                f"{str(condition).title()}"
            )
        )

        self.forecast_detail_temperature.configure(
            text=temperature_text
        )

        self.forecast_detail_rain.configure(
            text=(
                f"Rain Probability: "
                f"{rain}%"
            )
        )

        self.forecast_detail_analysis.configure(
            text=f"Analysis: {analysis}"
        )

    # =========================================================
    # HOVER EFFECT
    # =========================================================

    def bind_card_hover(
        self,
        card
    ):

        def on_enter(event):

            try:

                card.configure(
                    fg_color=self.hover_color
                )

            except Exception:
                pass

        def on_leave(event):

            try:

                selected_card = False

                if hasattr(
                    self,
                    "forecast_cards"
                ):

                    for item in self.forecast_cards:

                        if (
                            item.get("card")
                            is card
                        ):

                            selected_card = (
                                self.selected_forecast_index
                                == self.forecast_cards.index(item)
                            )
                            break

                if selected_card:

                    card.configure(
                        fg_color=self.accent_color
                    )

                else:

                    card.configure(
                        fg_color=self.card_color_2
                    )

            except Exception:
                pass

        card.bind(
            "<Enter>",
            on_enter
        )

        card.bind(
            "<Leave>",
            on_leave
        )

    # =========================================================
    # LOADING ANIMATION
    # =========================================================

    def start_loading_animation(self):

        self._loading_active = True
        self._loading_step = 0

        self.animate_loading()

    def stop_loading_animation(self):

        self._loading_active = False

    def animate_loading(self):

        if not self._loading_active:

            return

        dots = "." * (
            self._loading_step % 4
        )

        self.status_label.configure(
            text=f"Fetching weather{dots}",
            text_color=self.secondary_text
        )

        self._loading_step += 1

        self.after(
            350,
            self.animate_loading
        )

    # =========================================================
    # TEMPERATURE PULSE
    # =========================================================

    def animate_temperature_pulse(self):

        phase = (
            self._pulse_step % 40
        )

        distance = abs(
            20 - phase
        )

        factor = (
            1 - (distance / 20) * 0.18
        )

        r = int(
            77 * factor
        )

        g = int(
            166 * factor
        )

        b = int(
            255 * factor
        )

        self.temperature_label.configure(
            text_color=(
                f"#{r:02X}{g:02X}{b:02X}"
            )
        )

        self._pulse_step += 1

        self.after(
            100,
            self.animate_temperature_pulse
        )

    # =========================================================
    # WEATHER ICON HANDLER
    # =========================================================

    def set_weather_icon(
        self,
        label,
        condition,
        size=(64, 64)
    ):

        # -----------------------------------------------------
        # PNG ICON
        # -----------------------------------------------------

        if self.weather_visuals:

            try:

                self.weather_visuals.set_icon(
                    label,
                    condition,
                    size=size
                )

                return

            except (
                FileNotFoundError,
                OSError
            ):

                pass

        # -----------------------------------------------------
        # EMOJI FALLBACK
        # -----------------------------------------------------

        text = str(
            condition
        ).lower()

        if (
            "thunderstorm" in text
            or "storm" in text
        ):

            icon = "⛈"

        elif (
            "snow" in text
            or "sleet" in text
            or "ice" in text
        ):

            icon = "❄"

        elif (
            "rain" in text
            or "drizzle" in text
            or "shower" in text
        ):

            icon = "🌧"

        elif "clear" in text:

            icon = "☀"

        elif (
            "cloud" in text
            or "overcast" in text
        ):

            icon = "☁"

        else:

            icon = "☁"

        label.configure(
            image=None,
            text=icon
        )

    # =========================================================
    # SEARCH HISTORY
    # =========================================================

    def add_to_search_history(self, city):

        city = str(city).strip()

        if not city:
            return

        self.search_history = [
            item
            for item in self.search_history
            if item.lower() != city.lower()
        ]

        self.search_history.insert(
            0,
            city
        )

        self.search_history = (
            self.search_history[:5]
        )

        if hasattr(
            self,
            "history_combo"
        ):
            values = (
                self.search_history
                if self.search_history
                else ["Recent searches"]
            )

            self.history_combo.configure(
                values=values
            )

            self.history_combo.set(
                self.search_history[0]
            )

    def select_history_city(self, city):

        if not city or city == "Recent searches":
            return

        self.city_entry.delete(
            0,
            "end"
        )

        self.city_entry.insert(
            0,
            city
        )

        self.search_weather()

    # =========================================================
    # CLEAR DASHBOARD
    # =========================================================

    def clear_dashboard(self):

        self.stop_loading_animation()

        self.current_weather = None
        self.current_city = ""
        self.forecast_data = None
        self.air_quality_data = None
        self.selected_forecast_index = None

        self.city_entry.delete(
            0,
            "end"
        )

        self.current_location_label.configure(
            text="Current location: --"
        )

        self.status_label.configure(
            text="Enter a city to get weather information",
            text_color=self.secondary_text
        )

        self.updated_label.configure(
            text="Last updated: --"
        )

        self.city_label.configure(
            text="--"
        )

        self.temperature_label.configure(
            text="-- °C"
        )

        self.condition_label.configure(
            text="Condition: --"
        )

        self.feels_label.configure(
            text="Feels Like: -- °C"
        )

        self.humidity_label.configure(
            text="Humidity: --%"
        )

        self.pressure_label.configure(
            text="Pressure: -- hPa"
        )

        self.wind_label.configure(
            text="Wind Speed: -- m/s"
        )

        self.country_label.configure(
            text="Country: --"
        )

        self.set_weather_icon(
            self.current_weather_icon,
            "unknown",
            size=(72, 72)
        )

        for card in self.forecast_cards:

            card["day"].configure(
                text="--"
            )

            card["icon"].configure(
                image=None,
                text="☁"
            )

            card["condition"].configure(
                text="--"
            )

            card["temperature"].configure(
                text="-- / -- °C"
            )

            card["rain"].configure(
                text="Rain: --%"
            )

            card["card"].configure(
                fg_color=self.card_color_2
            )

        self.forecast_detail_day.configure(
            text="Click a forecast card to view details."
        )

        self.forecast_detail_condition.configure(
            text=""
        )

        self.forecast_detail_temperature.configure(
            text=""
        )

        self.forecast_detail_rain.configure(
            text=""
        )

        self.forecast_detail_analysis.configure(
            text=""
        )

        for widget, text_value in [
            (
                self.temperature_status,
                "Waiting..."
            ),
            (
                self.humidity_status,
                "Waiting..."
            ),
            (
                self.wind_status,
                "Waiting..."
            ),
            (
                self.rain_status,
                "Waiting..."
            )
        ]:

            widget.value_label.configure(
                text=text_value
            )

        self.recommendation_label.configure(
            text=(
                "Recommendation: Search for a city "
                "to get weather intelligence."
            )
        )

        self.aqi_label.configure(
            text="AQI: --"
        )

        self.aqi_status_label.configure(
            text="Status: Waiting..."
        )

        for label in self.pollutant_labels.values():

            label.configure(
                text="--"
            )

        self.average_temp_label.configure(
            text="Average Temperature: --"
        )

        self.highest_temp_label.configure(
            text="Highest Temperature: --"
        )

        self.lowest_temp_label.configure(
            text="Lowest Temperature: --"
        )

        self.average_rain_label.configure(
            text="Average Rain Probability: --"
        )

        self.highest_rain_label.configure(
            text="Highest Rain Probability: --"
        )

        self.aqi_summary_label.configure(
            text="AQI: --"
        )

        self.dominant_pollutant_label.configure(
            text="Dominant Pollutant: --"
        )

        self.weather_score_label.configure(
            text="-- / 100",
            text_color=self.accent_color
        )

        self.weather_score_progress.set(
            0
        )

        self.weather_score_progress.configure(
            progress_color=self.accent_color
        )

        self.weather_score_interpretation.configure(
            text="Waiting for weather data...",
            text_color=self.secondary_text
        )

        self.score_temperature_factor.configure(
            text="Temperature: Waiting..."
        )

        self.score_rain_factor.configure(
            text="Rain: Waiting..."
        )

        self.score_aqi_factor.configure(
            text="Air Quality: Waiting..."
        )

        self.score_pollutant_factor.configure(
            text="Dominant Pollutant: Waiting..."
        )

        self.refresh_button.configure(
            state="disabled",
            text="REFRESH"
        )

        if hasattr(
            self,
            "history_combo"
        ):
            self.history_combo.set(
                "Recent searches"
            )

    # =========================================================
    # USE MY LOCATION
    # =========================================================

    # =========================================================
    # REFRESH WEATHER
    # =========================================================

    def refresh_weather(self):

        if not self.current_city:

            self.status_label.configure(
                text="Search for a city first.",
                text_color=self.error_color
            )

            return

        self.city_entry.delete(
            0,
            "end"
        )

        self.city_entry.insert(
            0,
            self.current_city
        )

        self.search_weather()

    # =========================================================
    # SEARCH WEATHER
    # =========================================================

    def search_weather(self):

        city = self.city_entry.get().strip()

        if not city:

            self.status_label.configure(
                text="Please enter a city name.",
                text_color=self.error_color
            )

            return

        self.start_loading_animation()

        self.search_button.configure(
            state="disabled",
            text="LOADING..."
        )

        self.refresh_button.configure(
            state="disabled",
            text="REFRESHING..."
        )

        self.update_idletasks()

        try:

            # -------------------------------------------------
            # CURRENT WEATHER
            # -------------------------------------------------

            weather = get_current_weather(
                city
            )

            self.current_weather = (
                weather
            )

            # -------------------------------------------------
            # COORDINATES
            # -------------------------------------------------

            coordinates = weather.get(
                "coord",
                {}
            )

            latitude = coordinates[
                "lat"
            ]

            longitude = coordinates[
                "lon"
            ]

            # -------------------------------------------------
            # AIR QUALITY
            # -------------------------------------------------

            air_quality = get_air_quality(
                latitude,
                longitude
            )

            self.air_quality_data = (
                air_quality
            )

            # -------------------------------------------------
            # FORECAST
            # -------------------------------------------------

            forecast_raw = get_forecast(
                city
            )

            forecast = process_forecast(
                forecast_raw
            )

            self.forecast_data = (
                forecast
            )

            # -------------------------------------------------
            # UPDATE ALL SECTIONS
            # -------------------------------------------------

            self.update_current_weather(
                weather
            )

            self.update_forecast(
                forecast
            )

            if forecast:
                self.select_forecast(0)

            self.update_air_quality(
                air_quality
            )

            self.update_analytics_summary(
                forecast,
                air_quality
            )

            # -------------------------------------------------
            # UPDATE CHARTS
            # -------------------------------------------------

            self.charts.update_charts(
                forecast
            )

            self.charts.update_air_quality_chart(
                air_quality
            )

            # -------------------------------------------------
            # LOCATION
            # -------------------------------------------------

            actual_name = weather.get(
                "name",
                city
            )

            country = weather.get(
                "sys",
                {}
            ).get(
                "country",
                ""
            )

            if country:

                location = (
                    f"{actual_name}, "
                    f"{country}"
                )

            else:

                location = actual_name

            self.current_city = actual_name

            self.add_to_search_history(
                actual_name
            )

            self.current_location_label.configure(
                text=(
                    f"Current location: "
                    f"{location}"
                )
            )

            # -------------------------------------------------
            # LAST UPDATED
            # -------------------------------------------------

            timestamp = datetime.now().strftime(
                "%d %b %Y, %I:%M %p"
            )

            self.updated_label.configure(
                text=(
                    f"Last updated: "
                    f"{timestamp}"
                )
            )

            # -------------------------------------------------
            # SUCCESS
            # -------------------------------------------------

            self.stop_loading_animation()

            self.status_label.configure(
                text="Weather updated successfully",
                text_color=self.success_color
            )

        # -----------------------------------------------------
        # HTTP ERROR
        # -----------------------------------------------------

        except requests.exceptions.HTTPError as error:

            status_code = getattr(
                error.response,
                "status_code",
                None
            )

            if status_code == 404:

                message = (
                    "City not found. "
                    "Please check the spelling."
                )

            elif status_code == 401:

                message = (
                    "Invalid OpenWeather API key."
                )

            else:

                message = (
                    "Weather service returned "
                    "an error."
                )

            self.status_label.configure(
                text=message,
                text_color=self.error_color
            )

            print(
                "Weather HTTP Error:",
                error
            )

        # -----------------------------------------------------
        # CONNECTION ERROR
        # -----------------------------------------------------

        except requests.exceptions.ConnectionError as error:

            self.status_label.configure(
                text=(
                    "Unable to connect. "
                    "Check your internet connection."
                ),
                text_color=self.error_color
            )

            print(
                "Connection Error:",
                error
            )

        # -----------------------------------------------------
        # TIMEOUT
        # -----------------------------------------------------

        except requests.exceptions.Timeout as error:

            self.status_label.configure(
                text=(
                    "Weather service timed out. "
                    "Please try again."
                ),
                text_color=self.error_color
            )

            print(
                "Timeout Error:",
                error
            )

        # -----------------------------------------------------
        # DATA ERROR
        # -----------------------------------------------------

        except (
            KeyError,
            TypeError,
            ValueError
        ) as error:

            self.status_label.configure(
                text=(
                    "Weather data was incomplete "
                    "or invalid."
                ),
                text_color=self.error_color
            )

            print(
                "Weather Data Error:",
                error
            )

        # -----------------------------------------------------
        # UNEXPECTED ERROR
        # -----------------------------------------------------

        except Exception as error:

            self.status_label.configure(
                text=(
                    "Unable to fetch weather. "
                    "Please try again."
                ),
                text_color=self.error_color
            )

            print(
                "Unexpected Weather Error:",
                error
            )

        finally:

            self.stop_loading_animation()

            self.search_button.configure(
                state="normal",
                text="SEARCH WEATHER"
            )

            if self.current_weather is not None:

                self.refresh_button.configure(
                    state="normal",
                    text="REFRESH"
                )

            else:

                self.refresh_button.configure(
                    state="disabled",
                    text="REFRESH"
                )


    # =========================================================
    # UPDATE CURRENT WEATHER
    # =========================================================

    def update_current_weather(
        self,
        weather
    ):

        city = weather.get(
            "name",
            "--"
        )

        country = weather.get(
            "sys",
            {}
        ).get(
            "country",
            "--"
        )

        main = weather.get(
            "main",
            {}
        )

        wind = weather.get(
            "wind",
            {}
        )

        weather_list = weather.get(
            "weather",
            [{}]
        )

        temperature = main.get(
            "temp",
            "--"
        )

        feels_like = main.get(
            "feels_like",
            "--"
        )

        humidity = main.get(
            "humidity",
            "--"
        )

        pressure = main.get(
            "pressure",
            "--"
        )

        wind_speed = wind.get(
            "speed",
            "--"
        )

        condition = weather_list[
            0
        ].get(
            "description",
            "--"
        )

        # -----------------------------------------------------
        # ICON
        # -----------------------------------------------------

        self.set_weather_icon(
            self.current_weather_icon,
            condition,
            size=(72, 72)
        )

        # -----------------------------------------------------
        # UI
        # -----------------------------------------------------

        self.city_label.configure(
            text=f"{city}, {country}"
        )

        self.temperature_label.configure(
            text=f"{temperature} °C"
        )

        self.condition_label.configure(
            text=(
                f"Condition: "
                f"{condition.title()}"
            )
        )

        self.feels_label.configure(
            text=(
                f"Feels Like: "
                f"{feels_like} °C"
            )
        )

        self.humidity_label.configure(
            text=f"Humidity: {humidity}%"
        )

        self.pressure_label.configure(
            text=(
                f"Pressure: "
                f"{pressure} hPa"
            )
        )

        self.wind_label.configure(
            text=(
                f"Wind Speed: "
                f"{wind_speed} m/s"
            )
        )

        self.country_label.configure(
            text=f"Country: {country}"
        )

        # -----------------------------------------------------
        # INTELLIGENCE
        # -----------------------------------------------------

        self.update_intelligence(
            temperature,
            humidity,
            wind_speed
        )

    # =========================================================
    # UPDATE FORECAST
    # =========================================================

    def update_forecast(
        self,
        forecast
    ):

        for i, data in enumerate(
            forecast[:5]
        ):

            if i >= len(
                self.forecast_cards
            ):

                break

            card = self.forecast_cards[
                i
            ]

            day = data.get(
                "day",
                "--"
            )

            condition = data.get(
                "condition",
                "--"
            )

            # -------------------------------------------------
            # DAY
            # -------------------------------------------------

            card[
                "day"
            ].configure(
                text=str(day)
            )

            # -------------------------------------------------
            # ICON
            # -------------------------------------------------

            self.set_weather_icon(
                card["icon"],
                condition,
                size=(56, 56)
            )

            # -------------------------------------------------
            # CONDITION
            # -------------------------------------------------

            card[
                "condition"
            ].configure(
                text=str(
                    condition
                ).title()
            )

            # -------------------------------------------------
            # TEMPERATURE
            # -------------------------------------------------

            minimum = data.get(
                "min_temp",
                "--"
            )

            maximum = data.get(
                "max_temp",
                "--"
            )

            if (
                isinstance(
                    minimum,
                    (int, float)
                )
                and
                isinstance(
                    maximum,
                    (int, float)
                )
            ):

                card[
                    "temperature"
                ].configure(
                    text=(
                        f"{minimum:.1f}° / "
                        f"{maximum:.1f}°C"
                    )
                )

            else:

                temperature = data.get(
                    "temperature",
                    "--"
                )

                card[
                    "temperature"
                ].configure(
                    text=(
                        f"{temperature} °C"
                    )
                )

            # -------------------------------------------------
            # RAIN
            # -------------------------------------------------

            rain = data.get(
                "rain_probability",
                0
            )

            try:

                rain = float(
                    rain
                )

                if rain <= 1:

                    rain *= 100

                rain = round(
                    max(
                        0,
                        min(
                            100,
                            rain
                        )
                    )
                )

                card[
                    "rain"
                ].configure(
                    text=f"Rain: {rain}%"
                )

            except (
                ValueError,
                TypeError
            ):

                card[
                    "rain"
                ].configure(
                    text="Rain: --%"
                )

    # =========================================================
    # UPDATE INTELLIGENCE
    # =========================================================

    def update_intelligence(
        self,
        temperature,
        humidity,
        wind_speed
    ):

        try:

            temperature = float(
                temperature
            )

            humidity = float(
                humidity
            )

            wind_speed = float(
                wind_speed
            )

            rain_probability = 0

            if self.forecast_data:

                rain_probability = (
                    self.forecast_data[
                        0
                    ].get(
                        "rain_probability",
                        0
                    )
                )

            result = (
                get_weather_intelligence(
                    temperature,
                    humidity,
                    wind_speed,
                    rain_probability
                )
            )

            self.temperature_status.value_label.configure(
                text=result[
                    "temperature_status"
                ]
            )

            self.humidity_status.value_label.configure(
                text=result[
                    "humidity_status"
                ]
            )

            self.wind_status.value_label.configure(
                text=result[
                    "wind_status"
                ]
            )

            self.rain_status.value_label.configure(
                text=result[
                    "rain_status"
                ]
            )

            self.recommendation_label.configure(
                text=(
                    "Recommendation: "
                    + result[
                        "recommendation"
                    ]
                )
            )

        except Exception as error:

            print(
                "Intelligence Error:",
                error
            )

    # =========================================================
    # UPDATE AIR QUALITY
    # =========================================================

    def update_air_quality(
        self,
        air_quality
    ):

        try:

            aqi = air_quality.get(
                "aqi",
                0
            )

            statuses = {
                1: "Good",
                2: "Fair",
                3: "Moderate",
                4: "Poor",
                5: "Very Poor"
            }

            status = statuses.get(
                aqi,
                "Unknown"
            )

            self.aqi_label.configure(
                text=f"AQI: {aqi}"
            )

            self.aqi_status_label.configure(
                text=f"Status: {status}"
            )

            pollutant_keys = [
                "pm2_5",
                "pm10",
                "co",
                "no2",
                "o3",
                "so2",
                "nh3"
            ]

            for key in pollutant_keys:

                value = air_quality.get(
                    key,
                    "--"
                )

                if isinstance(
                    value,
                    (int, float)
                ):

                    value = round(
                        value,
                        2
                    )

                self.pollutant_labels[
                    key
                ].configure(
                    text=str(value)
                )

        except Exception as error:

            print(
                "Air Quality Error:",
                error
            )

    # =========================================================
    # UPDATE ANALYTICS
    # =========================================================

    def update_analytics_summary(
        self,
        forecast,
        air_quality
    ):

        try:

            stats = (
                calculate_forecast_statistics(
                    forecast
                )
            )

            # -------------------------------------------------
            # FORECAST STATISTICS
            # -------------------------------------------------

            self.average_temp_label.configure(
                text=(
                    "Average Temperature: "
                    f"{stats['average_temperature']} °C"
                )
            )

            self.highest_temp_label.configure(
                text=(
                    "Highest Temperature: "
                    f"{stats['highest_temperature']} °C"
                )
            )

            self.lowest_temp_label.configure(
                text=(
                    "Lowest Temperature: "
                    f"{stats['lowest_temperature']} °C"
                )
            )

            self.average_rain_label.configure(
                text=(
                    "Average Rain Probability: "
                    f"{stats['average_rain_probability']}%"
                )
            )

            self.highest_rain_label.configure(
                text=(
                    "Highest Rain Probability: "
                    f"{stats['highest_rain_probability']}%"
                )
            )

            # -------------------------------------------------
            # AIR QUALITY ANALYSIS
            # -------------------------------------------------

            air_stats = (
                analyze_air_quality(
                    air_quality
                )
            )

            self.aqi_summary_label.configure(
                text=(
                    f"AQI: {air_stats['aqi']} "
                    f"({air_stats['aqi_status']})"
                )
            )

            self.dominant_pollutant_label.configure(
                text=(
                    "Dominant Pollutant: "
                    f"{air_stats['dominant_pollutant']}"
                )
            )

            # -------------------------------------------------
            # WEATHER SCORE
            # -------------------------------------------------

            score_data = (
                calculate_weather_score(
                    stats[
                        "average_temperature"
                    ],
                    stats[
                        "average_rain_probability"
                    ],
                    air_stats[
                        "aqi"
                    ]
                )
            )

            score = score_data[
                "score"
            ]

            self.weather_score_label.configure(
                text=f"{score} / 100"
            )

            self.weather_score_progress.set(
                score / 100
            )

            # -------------------------------------------------
            # SCORE COLOR
            # -------------------------------------------------

            if score >= 80:

                score_color = (
                    self.success_color
                )

            elif score >= 60:

                score_color = (
                    self.accent_color
                )

            elif score >= 40:

                score_color = (
                    self.warning_color
                )

            else:

                score_color = (
                    self.error_color
                )

            self.weather_score_label.configure(
                text_color=score_color
            )

            self.weather_score_progress.configure(
                progress_color=score_color
            )

            self.weather_score_interpretation.configure(
                text=score_data[
                    "interpretation"
                ],
                text_color=score_color
            )

            # -------------------------------------------------
            # SCORE FACTORS
            # -------------------------------------------------

            average_temperature = (
                stats[
                    "average_temperature"
                ]
            )

            average_rain = (
                stats[
                    "average_rain_probability"
                ]
            )

            if (
                10
                <= average_temperature
                <= 35
            ):

                temperature_text = (
                    "Temperature: Comfortable"
                )

            elif average_temperature < 10:

                temperature_text = (
                    "Temperature: Cold impact"
                )

            else:

                temperature_text = (
                    "Temperature: Heat impact"
                )

            if average_rain < 20:

                rain_text = (
                    "Rain: Low risk"
                )

            elif average_rain < 50:

                rain_text = (
                    "Rain: Moderate risk"
                )

            elif average_rain < 75:

                rain_text = (
                    "Rain: High risk"
                )

            else:

                rain_text = (
                    "Rain: Very high risk"
                )

            self.score_temperature_factor.configure(
                text=temperature_text
            )

            self.score_rain_factor.configure(
                text=rain_text
            )

            self.score_aqi_factor.configure(
                text=(
                    "Air Quality: "
                    f"{air_stats['aqi_status']}"
                )
            )

            self.score_pollutant_factor.configure(
                text=(
                    "Dominant Pollutant: "
                    f"{air_stats['dominant_pollutant']}"
                )
            )

        except Exception as error:

            print(
                "Analytics Error:",
                error
            )


# =============================================================
# RUN APPLICATION
# =============================================================

if __name__ == "__main__":

    app = WeatherDashboard()

    app.mainloop()