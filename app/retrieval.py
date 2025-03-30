import faiss
import numpy as np
from typing import List
from loguru import logger

class VectorDatabase:
    """Manages FAISS-based document retrieval."""

    def __init__(self, embedding_dim: int = 384):
        logger.info("Initializing FAISS index")
        self.index = faiss.IndexFlatL2(embedding_dim)  
        self.documents = []  # Stores original text data

    def add_document(self, text: str, embedding: np.ndarray):
        """Adds a document and its embedding to the FAISS index."""
        self.index.add(np.array([embedding]))
        self.documents.append(text)

    def search(self, query_embedding: np.ndarray, top_k: int = 3) -> List[str]:
        """Finds the most similar documents for a query."""
        _, indices = self.index.search(np.array([query_embedding]), top_k)
        return [self.documents[i] for i in indices[0]]

vector_db = VectorDatabase()
