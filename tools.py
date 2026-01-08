# tools.py

from ddgs import DDGS
import random


# ---------------- WEATHER TOOL ---------------- #

class WeatherTool:
    """
    Simulates weather conditions for a given city.
    Useful for travel advice and planning.
    """

    CONDITIONS = ["sunny", "cloudy", "rainy", "stormy", "windy"]

    def get_weather(self, city: str) -> dict:
        return {
            "city": city,
            "temperature": random.randint(18, 35),
            "condition": random.choice(self.CONDITIONS),
            "humidity": random.randint(40, 90),
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
