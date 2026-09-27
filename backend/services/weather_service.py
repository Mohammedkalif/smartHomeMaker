import os
from datetime import datetime, timedelta
from typing import Optional

import httpx
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "").strip()
WEATHER_PROVIDER = os.getenv("WEATHER_PROVIDER", "openweathermap").strip().lower()


def _recommendation(condition: str, rain_probability: Optional[int]) -> str:
    text = (condition or "").lower()
    if rain_probability is not None and rain_probability >= 50:
        return "Rain is expected today. Carry an umbrella."
    if "rain" in text or "drizzle" in text or "thunder" in text:
        return "Rain is expected today. Carry an umbrella."
    if "storm" in text:
        return "Stormy weather is likely. Stay indoors if possible."
    if "snow" in text:
        return "Cold and snowy conditions. Wear warm clothes."
    if "cloud" in text:
        return "Cloudy skies today. A light jacket may be useful."
    if "clear" in text or "sun" in text:
        return "Pleasant weather. A good day for outdoor cooking or drying clothes."
    return "Check the sky before heading out and dress comfortably."


def _from_open_meteo(city: str) -> dict:
    with httpx.Client(timeout=15.0) as client:
        geo = client.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1},
        )
        geo.raise_for_status()
        data = geo.json()
        results = data.get("results") or []
        if not results:
            return {"error": f"Could not find weather for {city}."}

        place = results[0]
        forecast = client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": place["latitude"],
                "longitude": place["longitude"],
                "current": "temperature_2m,relative_humidity_2m,weather_code,precipitation_probability",
                "daily": "precipitation_probability_max",
                "hourly": "precipitation_probability",
                "timezone": "auto",
            },
        )
        forecast.raise_for_status()
        weather = forecast.json()
        current = weather.get("current") or {}
        daily = weather.get("daily") or {}
        code = current.get("weather_code", 0)
        condition = _weather_code_to_text(code)
        rain_probability = None
        probs = daily.get("precipitation_probability_max") or []
        if probs:
            rain_probability = int(probs[0])
        elif current.get("precipitation_probability") is not None:
            rain_probability = int(current["precipitation_probability"])
        hourly_times = (weather.get("hourly") or {}).get("time") or []
        hourly_probabilities = (weather.get("hourly") or {}).get("precipitation_probability") or []
        now = datetime.fromisoformat((current.get("time") or datetime.now().isoformat()).replace("Z", "+00:00")).replace(tzinfo=None)
        rain_soon_probability = max((int(probability or 0) for timestamp, probability in zip(hourly_times, hourly_probabilities) if now <= datetime.fromisoformat(timestamp) <= now + timedelta(hours=3)), default=0)

        return {
            "city": place.get("name", city),
            "temperature": current.get("temperature_2m"),
            "condition": condition,
            "humidity": current.get("relative_humidity_2m"),
            "rain_probability": rain_probability,
            "rain_soon": rain_soon_probability >= 50,
            "rain_soon_probability": rain_soon_probability,
            "recommendation": _recommendation(condition, rain_probability),
            "source": "open-meteo",
        }


def _weather_code_to_text(code: int) -> str:
    mapping = {
        0: "Clear",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Fog",
        51: "Light drizzle",
        61: "Rain",
        63: "Rain",
        65: "Heavy rain",
        80: "Rain showers",
        95: "Thunderstorm",
    }
    return mapping.get(code, "Mixed conditions")


def _from_openweathermap(city: str) -> dict:
    if not WEATHER_API_KEY or WEATHER_API_KEY == "your_weather_api_key_here":
        return _from_open_meteo(city)

    with httpx.Client(timeout=15.0) as client:
        response = client.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": city, "appid": WEATHER_API_KEY, "units": "metric"},
        )
        if response.status_code == 404:
            return {"error": f"Could not find weather for {city}."}
        response.raise_for_status()
        data = response.json()

        rain_probability = None
        forecast = client.get(
            "https://api.openweathermap.org/data/2.5/forecast",
            params={"q": city, "appid": WEATHER_API_KEY, "units": "metric", "cnt": 1},
        )
        if forecast.status_code == 200:
            items = forecast.json().get("list") or []
            if items and items[0].get("pop") is not None:
                rain_probability = int(round(items[0]["pop"] * 100))

        condition = (data.get("weather") or [{}])[0].get("description", "Unknown")
        main = data.get("main") or {}
        return {
            "city": data.get("name", city),
            "temperature": main.get("temp"),
            "condition": condition.title(),
            "humidity": main.get("humidity"),
            "rain_probability": rain_probability,
            "recommendation": _recommendation(condition, rain_probability),
            "source": "openweathermap",
        }


def get_weather(city: str) -> dict:
    city = (city or "").strip()
    if not city:
        return {"error": "Please provide a city name."}

    try:
        if WEATHER_PROVIDER in ("open-meteo", "openmeteo"):
            return _from_open_meteo(city)
        return _from_openweathermap(city)
    except httpx.HTTPError:
        return {
            "error": "Weather service is unavailable right now. Please try again later."
        }
