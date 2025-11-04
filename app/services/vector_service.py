import faiss
import numpy as np
from typing import List, Optional, Dict, Any, Union
import os
import logging
import json
from pathlib import Path
from langchain_core.documents import Document
from app.services.embedding_service import LocalEmbeddingService
from app.services.knowledge_loader import KnowledgeLoader

# Configure logging
logger = logging.getLogger("vector_service")

# Constants
VECTOR_STORE_DIR = Path("data")
VECTOR_STORE_DIR.mkdir(exist_ok=True, parents=True)
INDEX_FILE = VECTOR_STORE_DIR / "vector_index.faiss"
METADATA_FILE = VECTOR_STORE_DIR / "documents_metadata.json"

class VectorDatabaseService:
    def __init__(self, embedding_service: Optional[LocalEmbeddingService] = None):
        """Initialize the vector database service.
        
        Args:
            embedding_service: Optional custom embedding service. If not provided, 
                             a default LocalEmbeddingService will be used.
        """
        try:
            logger.info("Initializing VectorDatabaseService...")
            
            # Initialize embedding service
            self.embedding_service = embedding_service or LocalEmbeddingService()
            self.embedding_dim = self.embedding_service.get_embedding_dimension()
            
            # Initialize FAISS index
            self.index = None
            self.documents: List[Document] = []
            self.initialized = False
            
            logger.info(f"VectorDatabaseService initialized with embedding dimension: {self.embedding_dim}")
            
        except Exception as e:
            logger.error(f"Failed to initialize VectorDatabaseService: {str(e)}")
            raise

    def get_status(self) -> Dict[str, Any]:
        """Get the status of the vector database."""
        return {
            "initialized": self.initialized,
            "document_count": len(self.documents)
        }

    def is_initialized(self) -> bool:
        """Check if the vector database is initialized."""
        return self.initialized

    def get_document_count(self) -> int:
        """Get the number of documents in the vector database."""
        return len(self.documents)

    async def initialize_knowledge_base(self, force_rebuild: bool = False):
        """Initialize the knowledge base with documents and their embeddings.
        
        Args:
            force_rebuild: If True, rebuild the index even if it exists.
        """
        try:
            # Check if we can load existing index
            if not force_rebuild and await self._load_existing_index():
                logger.info("Successfully loaded existing vector index")
                self.initialized = True
                return
                
            logger.info("Starting knowledge base initialization...")
            knowledge_loader = KnowledgeLoader()
            
            # Load documents
            logger.info("Loading documents...")
            documents: List[Document] = await knowledge_loader.load_all_documents()
            if not documents:
                logger.warning("No documents found in knowledge base")
                self.initialized = True  # Mark as initialized even with no documents
                return
                
            self.documents = documents
            
            # Generate embeddings in batches
            logger.info(f"Generating embeddings for {len(self.documents)} documents...")
            texts = [doc.page_content for doc in self.documents]
            embeddings = await self.embedding_service.embed_documents(texts)
            
            if not embeddings or len(embeddings) == 0:
                raise ValueError("No embeddings were generated for the documents")
                
            # Initialize FAISS index
            logger.info(f"Initializing FAISS index with dimension {self.embedding_dim}...")
            self.index = faiss.IndexFlatL2(self.embedding_dim)
            # Convert to numpy array and normalize
            vectors = np.array(embeddings).astype('float32')
            faiss.normalize_L2(vectors)  # Normalize for cosine similarity
            
            # Create and populate FAISS index
            self.index = faiss.IndexFlatIP(self.embedding_dim)  # Inner product for cosine similarity
            self.index.add(vectors)
            
            # Save the index and metadata
            await self._save_index()
            
            self.initialized = True
            logger.info(f"Knowledge base initialized with {len(self.documents)} documents")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing knowledge base: {str(e)}")
            self.initialized = False
            raise

    async def _load_existing_index(self) -> bool:
        """Load existing FAISS index and metadata if they exist.
        
        Returns:
            bool: True if loading was successful, False otherwise.
        """
        try:
            if not INDEX_FILE.exists() or not METADATA_FILE.exists():
                logger.info("No existing index found, will create a new one")
                return False
                
            logger.info("Loading existing vector index...")
            self.index = faiss.read_index(str(INDEX_FILE))
            
            with open(METADATA_FILE, 'r', encoding='utf-8') as f:
                # Load raw data and convert back to Document objects
                loaded_data = json.load(f)
                self.documents = [Document(page_content=d["page_content"], metadata=d["metadata"]) for d in loaded_data]
                
            logger.info(f"Loaded {len(self.documents)} documents from existing index")
            return True
            
        except Exception as e:
            logger.error(f"Error loading existing index: {str(e)}")
            return False
            
    async def _save_index(self):
        """Save the FAISS index and metadata to disk."""
        try:
            if self.index is not None:
                faiss.write_index(self.index, str(INDEX_FILE))
                
            # Save document metadata (convert Document objects to dicts)
            with open(METADATA_FILE, 'w', encoding='utf-8') as f:
                json.dump([{"page_content": d.page_content, "metadata": d.metadata} for d in self.documents], f, ensure_ascii=False, indent=2)
                
            logger.info(f"Saved vector index with {len(self.documents)} documents")
            
        except Exception as e:
            logger.error(f"Failed to save index: {str(e)}")
            raise

    async def similarity_search(
        self, 
        query: str, 
        language: Optional[str] = None,
        k: int = 5,
        score_threshold: float = 0.6
    ) -> List[Dict[str, Any]]:
        """Find similar documents.
        
        Args:
            query: The search query text.
            language: Optional language code for filtering results.
            k: Maximum number of results to return.
            score_threshold: Minimum similarity score (0-1) for results.
            
        Returns:
            List of matching documents with their scores.
        """
        try:
            if not self.initialized or self.index is None:
                raise RuntimeError("Vector database is not initialized.")

            query_embedding = await self.embedding_service.embed_query(query)
            query_vector = np.array([query_embedding]).astype('float32')
            faiss.normalize_L2(query_vector)

            distances, indices = self.index.search(query_vector, k)

            results = []
            for i in range(len(indices[0])):
                if distances[0][i] >= score_threshold:
                    doc_index = indices[0][i]
                    results.append({
                        "document": self.documents[doc_index].page_content,
                        "metadata": self.documents[doc_index].metadata,
                        "score": distances[0][i]
                    })
            return results
        except Exception as e:
            logger.error(f"Error in similarity search: {str(e)}")
            return []

class CachedVectorService(VectorDatabaseService):
    def __init__(self, embedding_service: Optional[LocalEmbeddingService] = None):
        super().__init__(embedding_service)
        self.cache = {}  # Simple cache, upgrade to Redis in production
    
    async def similarity_search(
        self, 
        query: str, 
        language: Optional[str] = None,
        k: int = 5,
        score_threshold: float = 0.6
    ) -> List[Dict[str, Any]]:
        """Find similar documents with caching.
        
        Args:
            query: The search query text.
            language: Optional language code for filtering results.
            k: Maximum number of results to return.
            score_threshold: Minimum similarity score (0-1) for results.
            
        Returns:
            List of matching documents with their scores.
        """
        cache_key = f"{query}_{language or 'any'}_{k}_{score_threshold}"
        
        try:
            if cache_key in self.cache:
                logger.debug(f"Cache hit for query: {query}")
                return self.cache[cache_key]
                
            # If not in cache, perform the search
            logger.debug(f"Cache miss for query: {query}")
            results = await super().similarity_search(
                query=query,
                language=language,
                k=k,
                score_threshold=score_threshold
            )
            
            # Cache the results
            self.cache[cache_key] = results
            return results
            
        except Exception as e:
            logger.error(f"Error in cached similarity search: {str(e)}")
            return []
