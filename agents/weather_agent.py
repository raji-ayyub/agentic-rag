from tools.weather_tool import WeatherTool

class WeatherAgent:
    def __init__(self):
        self.tool = WeatherTool()

    def run(self, city: str) -> str:
        data = self.tool.get_weather(city)

        if "error" in data:
            return "Unable to retrieve weather data."
        
        return (
            f"Weather in {data['city']}:\n"
            f"- Condition: {data['description']}\n"
            f"- Temperature: {data['temperature']}°C\n"
            f"- Humidity: {data['humidity']}%"


        )