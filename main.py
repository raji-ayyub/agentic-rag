# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from app import TravelAssistant, TravelState

app = FastAPI(title="Travel Assistant API")

assistant = TravelAssistant()


class QuestionRequest(BaseModel):
    question: str
    city: Optional[str] = None


class AnswerResponse(BaseModel):
    answer: str


@app.post("/ask", response_model=AnswerResponse)
def ask(req: QuestionRequest):
    state: TravelState = {
        "question": req.question,
        "city": req.city,
        "route": None,
        "answer": None
    }

    try:
        result = assistant.run(state)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"answer": result["answer"]}
