from typing import List
from sentence_transformers import SentenceTransformer
import os

class LocalEmbeddingService:
    def __init__(self):
        model_path = os.getenv("SENTENCE_TRANSFORMER_MODEL_PATH", 'all-MiniLM-L6-v2')
        # If model_path is a local directory, load from there. Otherwise, SentenceTransformer will download.
        self.model = SentenceTransformer(model_path)
        self.embedding_dim = 384  # Dimension for chosen model
    
    async def embed_text(self, text: str) -> List[float]:
        """Generate embeddings for text using local model"""
        embeddings = self.model.encode(text)
        return embeddings.tolist()
    
    async def embed_documents(self, documents: List[str]) -> List[List[float]]:
        """Batch embed multiple documents"""
        embeddings = self.model.encode(documents)
        return embeddings.tolist()
    
    def get_embedding_dimension(self) -> int:
        return self.embedding_dim
