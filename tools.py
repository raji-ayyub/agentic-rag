# tools.py

from ddgs import DDGS
import random
import os
import requests
from dotenv import load_dotenv

load_dotenv()


# ---------------- WEATHER TOOL ---------------- #

class WeatherTool:
    """
    uses realtime weather data from openweather map to get weather conditions for a given city.
    Useful for travel advice and planning.
    """

    CONDITIONS = ["sunny", "cloudy", "rainy", "stormy", "windy"]
    
    def get_weather_api(self, city: str) -> dict:
        url = "https://api.openweathermap.org/data/2.5/weather"
        WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

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
            "condition": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"]
        }


# ---------------- DICTIONARY TOOL ---------------- #

class DictionaryTool:
    """
    Simple dictionary lookup for travel-related terms.
    """

    DEFINITIONS = {
        "visa": "An official document allowing entry into a foreign country.",
        "passport": "A government-issued document for international travel.",
        "embassy": "An official office representing a country abroad.",
        "layover": "A short stay between connecting flights.",
        "customs": "Authorities controlling goods entering a country."
    }

    def lookup(self, word: str) -> str:
        return self.DEFINITIONS.get(
            word.lower(),
            "Definition not found."
        )


# ---------------- WEB SEARCH TOOL ---------------- #

class WebSearchTool:
    """
    Searches the web using DuckDuckGo.
    """

    def search(self, query: str) -> str:
        results = []

        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=3):
                results.append(f"- {r['title']}: {r['body']}")

        if not results:
            return "No relevant information found."

        return "\n".join(results)
