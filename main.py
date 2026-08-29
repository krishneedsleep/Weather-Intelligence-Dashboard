import customtkinter as ctk

from ui.dashboard import WeatherDashboard


# Application appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# Start application
app = WeatherDashboard()

app.mainloop()