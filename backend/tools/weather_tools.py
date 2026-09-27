from services.weather_service import get_weather as fetch_weather


def get_weather(city: str):
    return fetch_weather(city)
