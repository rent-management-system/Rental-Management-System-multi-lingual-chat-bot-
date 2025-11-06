import faiss
import numpy as np
from typing import List, Tuple, Optional
from app.knowledge_base import load_and_split_documents, embedding_model
from app.utils import logger

class FAISSVectorStore:
    _instance = None
    _index: Optional[faiss.IndexFlatL2] = None
    _documents: List[str] = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FAISSVectorStore, cls).__new__(cls)
            cls._instance._initialize_store()
        return cls._instance

    def _initialize_store(self):
        """Initializes the FAISS index and loads documents."""
        logger.info("Initializing FAISS vector store...")
        try:
            self._documents = load_and_split_documents()
            if not self._documents:
                logger.warning("No documents loaded for FAISS index.")
                return

            # Embed documents
            document_embeddings = embedding_model.embed_documents(self._documents)
            dimension = len(document_embeddings[0])
            
            # Create FAISS index
            self._index = faiss.IndexFlatL2(dimension)
            self._index.add(np.array(document_embeddings).astype('float32'))
            logger.info(f"FAISS index initialized with {len(self._documents)} documents.")
        except Exception as e:
            logger.error(f"Error initializing FAISS vector store: {e}")
            self._index = None # Ensure index is None on failure
            self._documents = []

    def search(self, query: str, k: int = 3) -> List[str]:
        """
        Searches the FAISS index for the top-k most similar documents.
        """
        if self._index is None:
            logger.warning("FAISS index not initialized. Attempting to re-initialize.")
            self._initialize_store()
            if self._index is None:
                logger.error("FAISS index failed to initialize. Cannot perform search.")
                return []

        try:
            query_embedding = embedding_model.embed_query(query)
            D, I = self._index.search(np.array([query_embedding]).astype('float32'), k)
            
            results = []
            for i in I[0]:
                if i != -1: # -1 indicates no result found for that slot
                    results.append(self._documents[i])
            return results
        except Exception as e:
            logger.error(f"Error during FAISS search: {e}")
            return []

# Global instance for lazy loading
faiss_vector_store = FAISSVectorStore()

if __name__ == "__main__":
    # Example usage
    print("Testing FAISSVectorStore...")
    store = FAISSVectorStore()
    
    # Ensure the store is initialized
    if store._index:
        print(f"FAISS index has {store._index.ntotal} documents.")
        
        query_en = "What property types are available?"
        results_en = store.search(query_en, k=2)
        print(f"\nSearch results for '{query_en}':")
        for r in results_en:
            print(f"- {r[:100]}...")

        query_am = "የኪራይ አስተዳደር ስርዓት ምንድን ነው?"
        results_am = store.search(query_am, k=2)
        print(f"\nSearch results for '{query_am}':")
        for r in results_am:
            print(f"- {r[:100]}...")
    else:
        print("FAISS store not initialized, check logs for errors.")
