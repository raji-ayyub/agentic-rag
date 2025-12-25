import requests

from config import WEATHER_API_KEY

class WeatherTool:
    """
    Tool for real-time weather data.
    """

    def get_weather(self, city: str) -> dict:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": WEATHER_API_KEY,
            "units": "metric"
        }

        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code != 200:
            return {"error": data.get("message", "Weather API error")}
        
        return {
            "city": city,
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"]
        }