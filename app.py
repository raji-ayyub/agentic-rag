# app.py

from typing import TypedDict, Optional, List
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import (
    HumanMessage,
    ToolMessage,
    AIMessage,
    BaseMessage,
)
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END

from tools import WeatherTool, DictionaryTool, WebSearchTool

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


# =======================
# STATE

class TravelState(TypedDict):
    question: str
    city: Optional[str]
    messages: List[BaseMessage]
    answer: Optional[str]




# =======================
# TOOL INSTANCES

weather_tool = WeatherTool()
dictionary_tool = DictionaryTool()
search_tool = WebSearchTool()




# =======================
# TOOL WRAPPERS

@tool
def get_weather(city: str) -> str:
    """Get current weather conditions for a city."""
    data = weather_tool.get_weather_api(city)
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
TOOL_MAP = {
    "get_weather": get_weather,
    "define_word": define_word,
    "web_search": web_search,
}


# =======================
# LLM (with tools)

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=api_key,
    temperature=0,
).bind_tools(TOOLS)


# =======================
# GRAPH NODES

def llm_node(state: TravelState) -> TravelState:
    """Call the LLM with current messages."""
    response = llm.invoke(state["messages"])
    state["messages"].append(response)
    return state


def tool_node(state: TravelState) -> TravelState:
    """Execute the tool chosen by the LLM."""
    last_message = state["messages"][-1]

    if not isinstance(last_message, AIMessage):
        return state

    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        tool_call_id = tool_call["id"]

        tool_fn = TOOL_MAP.get(tool_name)
        if not tool_fn:
            continue

        result = tool_fn.invoke(tool_args)

        state["messages"].append(
            ToolMessage(
                tool_call_id=tool_call_id,
                name=tool_name,
                content=result,
            )
        )

    return state


def should_continue(state: TravelState) -> str:
    """
    Decide whether to continue tool execution or finish.
    """
    last_message = state["messages"][-1]

    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "tools"

    return "end"


def finalize_answer(state: TravelState) -> TravelState:
    """Extract final answer from the last assistant message."""
    for msg in reversed(state["messages"]):
        if isinstance(msg, AIMessage) and msg.content:
            state["answer"] = msg.content
            break
    return state


# =======================
# BUILD GRAPH

graph = StateGraph(TravelState)

graph.add_node("llm", llm_node)
graph.add_node("tools", tool_node)
graph.add_node("final", finalize_answer)

graph.set_entry_point("llm")

graph.add_conditional_edges(
    "llm",
    should_continue,
    {
        "tools": "tools",
        "end": "final",
    },
)

graph.add_edge("tools", "llm")
graph.add_edge("final", END)

app_graph = graph.compile()



class TravelAssistant:
    """
    LangGraph-powered travel assistant.
    Public interface remains unchanged.
    """

    def run(self, state: TravelState) -> TravelState:
        initial_state: TravelState = {
            "question": state["question"],
            "city": state.get("city"),
            "messages": [
                HumanMessage(
                    content=(
                        "You are a helpful travel assistant.\n"
                        "Use tools when appropriate.\n\n"
                        f"User question: {state['question']}\n"
                        f"City (if provided): {state.get('city')}"
                    )
                )
            ],
            "answer": None,
        }

        return app_graph.invoke(initial_state)
