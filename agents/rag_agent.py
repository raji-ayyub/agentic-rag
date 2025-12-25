from langchain_openai import ChatOpenAI
from config import LLM_MODEL

class RAGAgent:
    def __init__(self, retriever):
        self.retriever = retriever
        self.llm = ChatOpenAI(model=LLM_MODEL)

    def run(self, question: str) -> str:
        docs = self.retriever.invoke(question)
        context = "\n".join(d.page_content for d in docs)

        prompt = f"""
Use the context below to answer the question.

Context:
{context}

Question:
{question}
"""
        return self.llm.invoke(prompt).content