from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import PDF_DIR
import os

class WeatherDocLoader:
    """
    Loads and splits multiple weather PDFs.
    """

    def load_documents(self):
        documents = []

        if not os.path.exists(PDF_DIR):
            raise FileNotFoundError(f"PDF directory not found: {PDF_DIR}")

        for file in os.listdir(PDF_DIR):
            if file.lower().endswith(".pdf"):
                loader = PyPDFLoader(os.path.join(PDF_DIR, file))
                documents.extend(loader.load())

        if not documents:
            raise ValueError("No PDF documents were loaded.")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

        return splitter.split_documents(documents)