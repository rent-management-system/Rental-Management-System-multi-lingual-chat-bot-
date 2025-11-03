from typing import List
from sentence_transformers import SentenceTransformer

class LocalEmbeddingService:
    def __init__(self):
        # Use multi-lingual model for all languages
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
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
