import customtkinter as ctk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class WeatherCharts:

    def __init__(self, parent):

        self.parent = parent

        # =====================================================
        # MAIN CHART FRAME
        # =====================================================

        self.frame = ctk.CTkFrame(
            parent,
            corner_radius=15,
            fg_color="#17232E"
        )

        # =====================================================
        # TITLE
        # =====================================================

        self.title_label = ctk.CTkLabel(
            self.frame,
            text="WEATHER ANALYTICS",
            font=("Arial", 20, "bold"),
            text_color="#FFFFFF"
        )

        self.title_label.pack(
            anchor="w",
            padx=25,
            pady=(20, 10)
        )

        # =====================================================
        # TEMPERATURE CHART
        # =====================================================

        self.temperature_figure = Figure(
            figsize=(10, 4),
            dpi=100,
            facecolor="#17232E"
        )

        self.temperature_axis = (
            self.temperature_figure.add_subplot(111)
        )

        self.temperature_canvas = FigureCanvasTkAgg(
            self.temperature_figure,
            master=self.frame
        )

        self.temperature_canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        # =====================================================
        # RAIN PROBABILITY CHART
        # =====================================================

        self.rain_figure = Figure(
            figsize=(10, 4),
            dpi=100,
            facecolor="#17232E"
        )

        self.rain_axis = (
            self.rain_figure.add_subplot(111)
        )

        self.rain_canvas = FigureCanvasTkAgg(
            self.rain_figure,
            master=self.frame
        )

        self.rain_canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        # =====================================================
        # AIR QUALITY CHART
        # =====================================================

        self.air_quality_figure = Figure(
            figsize=(10, 5),
            dpi=100,
            facecolor="#17232E"
        )

        self.air_quality_axis = (
            self.air_quality_figure.add_subplot(111)
        )

        self.air_quality_canvas = FigureCanvasTkAgg(
            self.air_quality_figure,
            master=self.frame
        )

        self.air_quality_canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

    # =========================================================
    # SHOW CHARTS
    # =========================================================

    def show(self):

        self.frame.pack(
            fill="x",
            padx=60,
            pady=15
        )

    # =========================================================
    # STYLE CHART
    # =========================================================

    def style_axis(self, axis):

        axis.set_facecolor("#17232E")

        axis.tick_params(
            colors="#AAB4BE"
        )

        axis.xaxis.label.set_color(
            "#AAB4BE"
        )

        axis.yaxis.label.set_color(
            "#AAB4BE"
        )

        axis.title.set_color(
            "#FFFFFF"
        )

        for spine in axis.spines.values():

            spine.set_color(
                "#2D4050"
            )

        axis.grid(
            True,
            alpha=0.2
        )

    # =========================================================
    # UPDATE CHARTS
    # =========================================================

    def update_charts(
        self,
        forecast
    ):

        if not forecast:
            return

        # =====================================================
        # EXTRACT FORECAST DATA
        # =====================================================

        days = []
        temperatures = []
        rain_probabilities = []

        for data in forecast[:5]:

            days.append(
                str(
                    data.get(
                        "day",
                        "--"
                    )
                )
            )

            # -------------------------------------------------
            # TEMPERATURE
            # -------------------------------------------------

            min_temp = data.get(
                "min_temp"
            )

            max_temp = data.get(
                "max_temp"
            )

            if (
                isinstance(
                    min_temp,
                    (int, float)
                )
                and
                isinstance(
                    max_temp,
                    (int, float)
                )
            ):

                average_temperature = (
                    min_temp + max_temp
                ) / 2

                temperatures.append(
                    average_temperature
                )

            else:

                temperature = data.get(
                    "temperature",
                    0
                )

                try:

                    temperatures.append(
                        float(temperature)
                    )

                except (
                    ValueError,
                    TypeError
                ):

                    temperatures.append(0)

            # -------------------------------------------------
            # RAIN PROBABILITY
            # -------------------------------------------------

            rain = data.get(
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

                rain_probabilities.append(0)

        # =====================================================
        # TEMPERATURE CHART
        # =====================================================

        self.temperature_axis.clear()

        self.temperature_axis.plot(
            days,
            temperatures,
            marker="o",
            linewidth=2,
            markersize=7
        )

        self.temperature_axis.set_title(
            "5-Day Temperature Trend",
            fontsize=14,
            fontweight="bold"
        )

        self.temperature_axis.set_xlabel(
            "Day"
        )

        self.temperature_axis.set_ylabel(
            "Temperature (°C)"
        )

        self.style_axis(
            self.temperature_axis
        )

        # Temperature labels

        for day, temperature in zip(
            days,
            temperatures
        ):

            self.temperature_axis.annotate(
                f"{temperature:.1f}°C",
                (day, temperature),
                textcoords="offset points",
                xytext=(0, 8),
                ha="center",
                color="#FFFFFF",
                fontsize=9
            )

        self.temperature_figure.tight_layout()

        self.temperature_canvas.draw()

        # =====================================================
        # RAIN CHART
        # =====================================================

        self.rain_axis.clear()

        bars = self.rain_axis.bar(
            days,
            rain_probabilities
        )

        self.rain_axis.set_title(
            "Rain Probability",
            fontsize=14,
            fontweight="bold"
        )

        self.rain_axis.set_xlabel(
            "Day"
        )

        self.rain_axis.set_ylabel(
            "Probability (%)"
        )

        self.rain_axis.set_ylim(
            0,
            100
        )

        self.style_axis(
            self.rain_axis
        )

        # Rain percentage labels

        for bar, probability in zip(
            bars,
            rain_probabilities
        ):

            label_position = min(
                probability + 3,
                97
            )

            self.rain_axis.text(
                bar.get_x()
                + bar.get_width() / 2,
                label_position,
                f"{probability:.0f}%",
                ha="center",
                color="#FFFFFF",
                fontsize=9
            )

        self.rain_figure.tight_layout()

        self.rain_canvas.draw()

    # =========================================================
    # UPDATE AIR QUALITY CHART
    # =========================================================

    def update_air_quality_chart(
        self,
        air_quality
    ):

        if not air_quality:
            return

        # =====================================================
        # POLLUTANTS
        # =====================================================

        pollutant_names = [
            "PM2.5",
            "PM10",
            "CO",
            "NO₂",
            "O₃",
            "SO₂",
            "NH₃"
        ]

        pollutant_keys = [
            "pm2_5",
            "pm10",
            "co",
            "no2",
            "o3",
            "so2",
            "nh3"
        ]

        values = []

        for key in pollutant_keys:

            value = air_quality.get(
                key,
                0
            )

            try:

                values.append(
                    float(value)
                )

            except (
                ValueError,
                TypeError
            ):

                values.append(0)

        # =====================================================
        # CLEAR PREVIOUS CHART
        # =====================================================

        self.air_quality_axis.clear()

        # =====================================================
        # CREATE BAR CHART
        # =====================================================

        bars = self.air_quality_axis.bar(
            pollutant_names,
            values
        )

        self.air_quality_axis.set_title(
            "Air Pollutant Concentration",
            fontsize=14,
            fontweight="bold"
        )

        self.air_quality_axis.set_xlabel(
            "Pollutant"
        )

        self.air_quality_axis.set_ylabel(
            "Concentration (µg/m³)"
        )

        self.style_axis(
            self.air_quality_axis
        )

        # =====================================================
        # VALUE LABELS
        # =====================================================

        maximum_value = max(
            values
        ) if values else 0

        for bar, value in zip(
            bars,
            values
        ):

            if maximum_value > 0:

                offset = (
                    maximum_value * 0.02
                )

            else:

                offset = 0.1

            self.air_quality_axis.text(
                bar.get_x()
                + bar.get_width() / 2,
                value + offset,
                f"{value:.1f}",
                ha="center",
                color="#FFFFFF",
                fontsize=9
            )

        self.air_quality_figure.tight_layout()

        self.air_quality_canvas.draw()