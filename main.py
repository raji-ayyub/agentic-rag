# main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uvicorn

from app import TravelAssistant, TravelState
from langchain_core.messages import ToolMessage

app = FastAPI(
    title="Travel Assistant API",
    description="AI-powered travel assistant with weather, dictionary, and web search capabilities",
    version="1.0.0"
)

# ---------------- MIDDLEWARE ---------------- #

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

assistant = TravelAssistant()

# ---------------- MODELS ---------------- #

class TravelRequest(BaseModel):
    question: str
    city: Optional[str] = None


class TravelResponse(BaseModel):
    answer: str
    tool_used: Optional[str]
    city: Optional[str]
    success: bool


class HealthResponse(BaseModel):
    status: str
    version: str
    tools_available: List[str]


# ---------------- ENDPOINTS ---------------- #

@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        tools_available=["get_weather", "define_word", "web_search"]
    )


@app.post("/api/assist", response_model=TravelResponse)
async def travel_assist(request: TravelRequest):
    """
    Main endpoint for travel assistance.
    """
    try:
        # Build initial state for LangGraph
        state: TravelState = {
            "question": request.question,
            "city": request.city,
            "messages": [],
            "answer": None,
        }

        result = assistant.run(state)

        # Extract tool used (first tool invocation)
        tool_used = None
        messages = result.get("messages", [])

        for msg in messages:
            if isinstance(msg, ToolMessage):
                tool_used = msg.name
                break

        return TravelResponse(
            answer=result.get("answer") or "I couldn't process your request.",
            tool_used=tool_used,
            city=request.city,
            success=True
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )


@app.get("/api/tools")
async def list_tools():
    """List all available tools"""
    return {
        "tools": [
            {
                "name": "get_weather",
                "description": "Get current weather conditions for a city",
                "parameters": ["city"]
            },
            {
                "name": "define_word",
                "description": "Look up the meaning of a word",
                "parameters": ["word"]
            },
            {
                "name": "web_search",
                "description": "Search the web for travel-related information",
                "parameters": ["query"]
            }
        ]
    }


# ---------------- ENTRY POINT ---------------- #

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
