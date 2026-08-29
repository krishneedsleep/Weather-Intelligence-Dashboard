# Weather-Intelligence-Dashboard

A Python-based interactive desktop application that combines real-time weather data, 5-day forecasts, air-quality information, analytical visualizations, and rule-based weather intelligence into a single dashboard.

## Project Overview

The Weather Intelligence Dashboard is a desktop application developed using Python. It retrieves live environmental data through OpenWeather APIs and presents the information through an interactive graphical user interface.

Instead of displaying raw weather values separately, the application organizes the information into current-weather cards, forecast cards, air-quality metrics, charts, analytical summaries, weather intelligence, and a custom Weather Score.

The project was developed as a Mini Project for the B.Tech Computer Science and Engineering program at Uttaranchal University, Dehradun.

## Features

- Real-time weather information for searched cities
- City search using OpenWeather geocoding
- Current temperature and feels-like temperature
- Humidity, atmospheric pressure and wind speed
- Weather condition and weather icons
- 5-day weather forecast
- Daily minimum and maximum temperatures
- Rain probability
- Air Quality Index (AQI)
- Major pollutant measurements:
  - PM2.5
  - PM10
  - CO
  - NO₂
  - O₃
  - SO₂
  - NH₃
- Temperature trend visualization
- Rain probability visualization
- Air pollutant concentration chart
- Weather Intelligence classifications
- Weather recommendations
- Custom Weather Score from 0–100
- Refresh functionality
- Clear and search controls
- Scrollable dashboard interface
- Error handling for invalid locations and API failures
- Modular Python architecture

## Dashboard Sections

### Current Weather

Displays the latest weather conditions for the selected city, including:

- Temperature
- Feels-like temperature
- Humidity
- Pressure
- Wind speed
- Weather condition
- Country
- Last updated time

### 5-Day Forecast

Provides daily forecast cards containing:

- Date
- Weather condition
- Weather icon
- Minimum temperature
- Maximum temperature
- Rain probability

Selecting a forecast card displays additional information and analysis for that day.

### Air Quality

The air-quality section displays the AQI and individual pollutant concentrations.

The monitored pollutants include PM2.5, PM10, CO, NO₂, O₃, SO₂ and NH₃.

### Weather Analytics

The dashboard provides graphical analysis of environmental data through:

- 5-Day Temperature Trend
- Rain Probability
- Air Pollutant Concentration

These visualizations make it easier to compare forecast values and identify trends.

### Weather Intelligence

The application converts numerical weather information into simple classifications for:

- Temperature
- Humidity
- Wind
- Rain Risk

It also generates a short recommendation based on the available conditions.

### Weather Score

The Weather Score is a project-specific analytical indicator ranging from 0 to 100.

It uses factors such as:

- Average forecast temperature
- Average rain probability
- Air Quality Index

The score is intended to provide a simple overall interpretation of the current forecast and environmental conditions.

> The Weather Score is a custom project metric and is not an official meteorological standard.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application development |
| CustomTkinter | Graphical user interface |
| Requests | REST API communication |
| Pillow | Image and icon handling |
| Matplotlib | Data visualization |
| OpenWeather APIs | Weather, forecast, geocoding and air-quality data |

## Project Architecture

The application follows a modular architecture where different responsibilities are separated into individual services.

```text
User
  |
  v
Dashboard GUI
  |
  +----------------------+
  |                      |
  v                      v
Location Service     Weather Service
  |                      |
  v                      v
Geocoding API         Weather API
  |                      |
  +----------+-----------+
             |
             v
       Forecast Service
             |
             v
      Air Quality Service
             |
             v
      Analytics Service
             |
             v
    Intelligence Service
             |
             v
       Weather Charts
             |
             v
       Dashboard Output
