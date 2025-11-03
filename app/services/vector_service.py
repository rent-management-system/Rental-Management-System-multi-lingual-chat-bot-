import faiss
import numpy as np
from typing import List
from app.services.embedding_service import LocalEmbeddingService
from app.services.knowledge_loader import KnowledgeLoader

class VectorDatabaseService:
    def __init__(self):
        self.embedding_service = LocalEmbeddingService()
        self.index = None
        self.documents = []

    async def initialize_knowledge_base(self):
        knowledge_loader = KnowledgeLoader()
        documents = await knowledge_loader.load_all_documents()
        embeddings = await self.embedding_service.embed_documents(documents)
        self.documents = documents

        dimension = len(embeddings[0])
        self.index = faiss.IndexFlatL2(dimension)  # L2 distance index

        np_embeddings = np.array(embeddings).astype('float32')
        self.index.add(np_embeddings)

    async def similarity_search(self, query: str, language: str, k: int = 5) -> List[str]:
        query_embedding = await self.embedding_service.embed_text(query)
        np_query = np.array([query_embedding]).astype('float32')

        distances, indices = self.index.search(np_query, k)
        results = []
        for idx in indices[0]:
            if idx < len(self.documents):
                results.append(self.documents[idx])
        return results

class CachedVectorService(VectorDatabaseService):
    def __init__(self):
        super().__init__()
        self.cache = {}  # Simple cache, upgrade to Redis in production
    
    async def similarity_search(self, query: str, language: str, k: int = 5) -> List[str]:
        cache_key = f"{query}_{language}_{k}"
        
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        results = await super().similarity_search(query, language, k)
        self.cache[cache_key] = results
        
        return results
