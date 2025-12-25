from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from config import CHROMA_DIR

class WeatherVectorStore:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.store = None

    def build(self, documents):

        if not documents:
            raise ValueError("Cannot build vector store with empty documents.")
        self.store = Chroma.from_documents(
            documents,
            self.embeddings,
            persist_directory=CHROMA_DIR
        )

    def get_retriever(self):
        if self.store is None:
            raise RuntimeError("Vector store has not been built.")
        
        return self.store.as_retriever(search_kwargs={"k": 3})
    