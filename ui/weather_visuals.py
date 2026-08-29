from pathlib import Path
import customtkinter as ctk
from PIL import Image, ImageTk


class WeatherVisuals:

    ICONS = {
        "sun": "sun.png",
        "cloud": "cloud.png",
        "rain": "rain.png",
        "storm": "storm.png",
        "snow": "snow.png",
        "unknown": "unknown.png"
    }

    def __init__(self, dashboard):

        self.dashboard = dashboard

        self.assets_dir = (
            Path(__file__).resolve().parent.parent
            / "assets"
            / "weather"
        )

        self.icon_cache = {}

    # =========================================================
    # DETERMINE ICON TYPE
    # =========================================================

    def get_icon_type(self, condition):

        condition = str(
            condition
        ).lower()

        if (
            "thunderstorm" in condition
            or "storm" in condition
        ):
            return "storm"

        if (
            "snow" in condition
            or "sleet" in condition
            or "ice" in condition
        ):
            return "snow"

        if (
            "rain" in condition
            or "drizzle" in condition
            or "shower" in condition
        ):
            return "rain"

        if "clear" in condition:
            return "sun"

        if (
            "cloud" in condition
            or "overcast" in condition
        ):
            return "cloud"

        return "unknown"

    # =========================================================
    # LOAD ICON
    # =========================================================

    def get_icon(
        self,
        condition,
        size=(64, 64)
    ):

        icon_type = self.get_icon_type(
            condition
        )

        cache_key = (
            icon_type,
            size
        )

        if cache_key not in self.icon_cache:

            icon_path = (
                self.assets_dir
                / self.ICONS[icon_type]
            )

            image = Image.open(
                icon_path
            ).convert("RGBA")

            image.thumbnail(
                size,
                Image.Resampling.LANCZOS
            )

            self.icon_cache[
                cache_key
            ] = ImageTk.PhotoImage(
                image
            )

        return self.icon_cache[
            cache_key
        ]

    # =========================================================
    # SET ICON ON LABEL
    # =========================================================

    def set_icon(
        self,
        label,
        condition,
        size=(64, 64)
    ):

        icon = self.get_icon(
            condition,
            size
        )

        label.configure(
            image=icon,
            text=""
        )