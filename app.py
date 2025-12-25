# from rag.loader import WeatherDocLoader
# from rag.vectorstore import WeatherVectorStore
# from graph.weather_graph import WeatherGraph


# def main():
#     loader = WeatherDocLoader()
#     docs = loader.load_documents()

#     store = WeatherVectorStore()
#     store.build(docs)

#     graph = WeatherGraph(store.get_retriever())

#     question = input("Ask a weather question: ")

#     city=None

#     if "weather" in question.lower():
#         city = input("City: ")

#     result = graph.app.invoke({
#         "question": question,
#         "city": city
#     })

#     print ("\nAnswer:\n", result["answer"])

# if __name__ == "__main__":
#     main()





from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from rag.loader import WeatherDocLoader
from rag.vectorstore import WeatherVectorStore
from graph.weather_graph import WeatherGraph

class QuestionRequest(BaseModel):
    question: str
    city: Optional[str] = None

class AnswerResponse(BaseModel):
    answer: str

app = FastAPI(title="Agentic RAG Weather API")

loader = WeatherDocLoader()
docs = loader.load_documents()

store = WeatherVectorStore()
store.build(docs)

graph = WeatherGraph(store.get_retriever())


@app.post("/ask", response_model=AnswerResponse)
def ask_question(req: QuestionRequest):
    state_input = {"question": req.question, "city": req.city}

    try:
        result = graph.app.invoke(state_input)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"answer": result.get("answer", "No response available")}