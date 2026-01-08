# app.py

from typing import TypedDict, Optional, Any
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage

from tools import WeatherTool, DictionaryTool, WebSearchTool

import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


# ---------------- STATE ---------------- #

class TravelState(TypedDict):
    question: str
    city: Optional[str]
    answer: Optional[str]


# ---------------- TOOL WRAPPERS ---------------- #
# These wrappers expose your tools to the LLM

weather_tool = WeatherTool()
dictionary_tool = DictionaryTool()
search_tool = WebSearchTool()


@tool
def get_weather(city: str) -> str:
    """Get current weather conditions for a city."""
    data = weather_tool.get_weather(city)
    return (
        f"Weather in {data['city']}:\n"
        f"- Condition: {data['condition']}\n"
        f"- Temperature: {data['temperature']}°C\n"
        f"- Humidity: {data['humidity']}%"
    )


@tool
def define_word(word: str) -> str:
    """Look up the meaning of a word."""
    return dictionary_tool.lookup(word)


@tool
def web_search(query: str) -> str:
    """Search the web for travel-related information."""
    return search_tool.search(query)


TOOLS = [get_weather, define_word, web_search]


# ---------------- TRAVEL ASSISTANT ---------------- #

class TravelAssistant:
    """
    Tool-driven travel assistant.
    The LLM decides which tool to use.
    """

    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=api_key,
            temperature=0
        ).bind_tools(TOOLS)

    def run(self, state: TravelState) -> TravelState:
        messages = [
            HumanMessage(
                content=(
                    "You are a helpful travel assistant.\n"
                    "Use tools when appropriate.\n\n"
                    f"User question: {state['question']}\n"
                    f"City (if provided): {state.get('city')}"
                )
            )
        ]

        response = self.llm.invoke(messages)

        # If the LLM decided to call a tool
        if response.tool_calls:
            tool_call = response.tool_calls[0]
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            tool_map = {
                "get_weather": get_weather,
                "define_word": define_word,
                "web_search": web_search,
            }

            tool_result = tool_map[tool_name].invoke(tool_args)

            state["answer"] = tool_result
            return state

        # If no tool was needed
        state["answer"] = response.content
        return state
