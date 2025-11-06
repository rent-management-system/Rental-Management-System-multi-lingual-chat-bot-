import os
import logging
from threading import Lock

logger = logging.getLogger(__name__)
_lock = Lock()
_model = None

def get_embedding_model():
    global _model
    if _model is not None:
        return _model
    with _lock:
        if _model is None:
            model_name = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
            logger.info("Loading embedding model: %s", model_name)
            from sentence_transformers import SentenceTransformer
            _model = SentenceTransformer(model_name, device="cpu")
    return _model
