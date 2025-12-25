from langgraph.graph import StateGraph, END
from state import WeatherState

from agents.router import RouterAgent
from agents.weather_agent import WeatherAgent
from agents.rag_agent import RAGAgent

class WeatherGraph:
    def __init__(self, retriever):
        self.router = RouterAgent()
        self.weather_agent = WeatherAgent()
        self.rag_agent = RAGAgent(retriever)

        self.graph = StateGraph(WeatherState)

        self.graph.add_node("route", self.route)
        self.graph.add_node("weather", self.weather)
        self.graph.add_node("rag", self.rag)


        self.graph.set_entry_point("route")


        self.graph.add_conditional_edges(
            "route",
            lambda state: state["route"],
            {
                "weather": "weather",
                "rag": "rag"
            }
        )

        self.graph.add_edge("weather", END)
        self.graph.add_edge("rag", END)

        self.app = self.graph.compile()

    
    def route(self, state):
        route = self.router.route(state["question"])

        if route not in ("weather", "rag"):
            route = "rag"
        
        state["route"] = route
        return state
    
    def weather(self, state):
        state["answer"] = self.weather_agent.run(state["city"])
        return state
    
    def rag(self, state):
        state["answer"] = self.rag_agent.run(state["question"])
        return state