import faiss
import numpy as np
from typing import List, Tuple, Optional
from app.knowledge_base import load_and_split_documents, embedding_model
from app.utils import logger
import threading

class FAISSVectorStore:
    _instance = None
    _lock = threading.Lock()
    _index: Optional[faiss.IndexFlatL2] = None
    _documents: List[str] = []

    def __new__(cls):
        # Double-checked locking for thread-safe singleton creation
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(FAISSVectorStore, cls).__new__(cls)
        return cls._instance

    def _initialize_store(self):
        """Initializes the FAISS index and loads documents."""
        # This method should only be called from within a lock
        if self._index is not None:
            logger.info("FAISS index already initialized.")
            return

        logger.info("Initializing FAISS vector store...")
        try:
            self._documents = load_and_split_documents()
            if not self._documents:
                logger.warning("No documents loaded for FAISS index.")
                return

            # Embed documents
            document_embeddings = embedding_model.embed_documents(self._documents)
            if not document_embeddings:
                logger.error("Embedding documents failed, no embeddings returned.")
                return
                
            dimension = len(document_embeddings[0])
            
            # Create FAISS index
            self._index = faiss.IndexFlatL2(dimension)
            self._index.add(np.array(document_embeddings).astype('float32'))
            logger.info(f"FAISS index initialized with {len(self._documents)} documents.")
        except Exception as e:
            logger.error(f"Error initializing FAISS vector store: {e}", exc_info=True)
            self._index = None # Ensure index is None on failure
            self._documents = []

    def get_index(self):
        """Returns the FAISS index, initializing it if necessary."""
        if self._index is None:
            with self._lock:
                # Check again inside the lock
                if self._index is None:
                    self._initialize_store()
        return self._index

    def search(self, query: str, k: int = 3) -> List[str]:
        """
        Searches the FAISS index for the top-k most similar documents.
        """
        index = self.get_index()
        if index is None:
            logger.error("FAISS index failed to initialize. Cannot perform search.")
            return []

        try:
            query_embedding = embedding_model.embed_query(query)
            D, I = index.search(np.array([query_embedding]).astype('float32'), k)
            
            results = []
            for i in I[0]:
                if i != -1: # -1 indicates no result found for that slot
                    results.append(self._documents[i])
            return results
        except Exception as e:
            logger.error(f"Error during FAISS search: {e}", exc_info=True)
            return []

# Global instance for lazy loading
faiss_vector_store = FAISSVectorStore()

if __name__ == "__main__":
    # Example usage
    print("Testing FAISSVectorStore...")
    
    # The index is now initialized lazily on the first search
    
    query_en = "What property types are available?"
    results_en = faiss_vector_store.search(query_en, k=2)
    print(f"\nSearch results for '{query_en}':")
    for r in results_en:
        print(f"- {r[:100]}...")

    query_am = "የኪራይ አስተዳደር ስርዓት ምንድን ነው?"
    results_am = faiss_vector_store.search(query_am, k=2)
    print(f"\nSearch results for '{query_am}':")
    for r in results_am:
        print(f"- {r[:100]}...")