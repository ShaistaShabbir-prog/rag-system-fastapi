from sentence_transformers import SentenceTransformer
import numpy as np
from loguru import logger

class EmbeddingModel:
    """Handles document embedding using a pre-trained transformer model."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        logger.info(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)

    def generate_embedding(self, text: str) -> np.ndarray:
        """Generates an embedding vector for a given text."""
        return self.model.encode([text])[0].astype("float32")

embedding_model = EmbeddingModel()  # Singleton instance
