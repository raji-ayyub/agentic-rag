from langchain_openai import ChatOpenAI
from config import LLM_MODEL


class RouterAgent:
    """
    Decides whether to use:
    - weather → real-time weather API
    - rag → document-based explanation
    """

    def __init__(self):
        self.llm = ChatOpenAI(model=LLM_MODEL, temperature=0)

    def route(self, question: str) -> str:
        prompt = f"""
You are a routing agent.

Return EXACTLY one word:
- weather → real-time weather (today, tomorrow, temperature, rain)
- rag → explanations, climate, definitions, concepts

Question: {question}

Answer:
"""

        response = self.llm.invoke(prompt)

        # Normalize output
        decision = response.content.strip().lower()

        # Explicit routing (NO ambiguity)
        if decision.startswith("weather"):
            return "weather"

        if decision.startswith("rag"):
            return "rag"

        # 🔒 HARD SAFETY FALLBACK (CRITICAL)
        return "rag"
