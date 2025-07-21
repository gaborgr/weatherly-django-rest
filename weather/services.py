import requests
from django.conf import settings


def get_coordinates(city_name, country_code="", api_key=settings.OPENWEATHER_API_KEY):
    geocode_url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {
        "q": f"{city_name},{country_code}" if country_code else city_name,
        "limit": 1,
        "appid": api_key,
    }
    try:
        response = requests.get(geocode_url, params=params).json()
        if response:
            return response[0]["lat"], response[0]["lon"]
        return None, None
    except Exception as e:
        print(f"Geocoding error: {e}")
        return None, None


def fetch_weather_by_coords(lat, lon, api_key=settings.OPENWEATHER_API_KEY):
    weather_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"lat": lat, "lon": lon, "appid": api_key, "units": "metric", "lang": "es"}
    try:
        response = requests.get(weather_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Weather API error: {e}")
        return None
