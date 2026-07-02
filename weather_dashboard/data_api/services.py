import requests
from django.conf import settings

from .models import WeatherReading


def fetch_weather(city="Kigali"):
    """Fetch current weather for a city and save it as a WeatherReading."""

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={settings.OWM_API_KEY}&units=metric"
    )
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

    data = resp.json()
    rain = data.get("rain", {})
    snow = data.get("snow", {})

    reading = WeatherReading.objects.create(
        city=city,
        temperature=data["main"]["temp"],
        feels_like=data["main"]["feels_like"],
        humidity=data["main"]["humidity"],
        pressure=data["main"]["pressure"],
        weather_desc=data["weather"][0]["description"],
        wind_speed=data["wind"]["speed"],
        precipitation=rain.get("1h", rain.get("3h", snow.get("1h", snow.get("3h", 0.0)))),
        cloud_cover=data.get("clouds", {}).get("all", 0.0),
    )
    return reading
