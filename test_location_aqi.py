from services.location_service import get_coordinates
from services.air_quality_service import get_air_quality


city = input("Enter city name: ")

try:
    # Get coordinates
    location = get_coordinates(city)

    print("\nLocation found!")
    print("-----------------------------")
    print("City:", location["name"])
    print("State:", location.get("state", "N/A"))
    print("Country:", location["country"])
    print("Latitude:", location["latitude"])
    print("Longitude:", location["longitude"])

    # Get air quality
    air_quality = get_air_quality(
        location["latitude"],
        location["longitude"]
    )

    print("\nAir Quality")
    print("-----------------------------")
    print("AQI:", air_quality["aqi"])
    print("CO:", air_quality["co"], "μg/m³")
    print("NO₂:", air_quality["no2"], "μg/m³")
    print("O₃:", air_quality["o3"], "μg/m³")
    print("SO₂:", air_quality["so2"], "μg/m³")
    print("PM2.5:", air_quality["pm2_5"], "μg/m³")
    print("PM10:", air_quality["pm10"], "μg/m³")
    print("NH₃:", air_quality["nh3"], "μg/m³")

except Exception as error:
    print("\nSomething went wrong:")
    print(error)