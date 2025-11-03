import logging

logger = logging.getLogger("rental_chatbot")
logger.setLevel(logging.INFO)

class VectorDBLogger:
    async def log_retrieval_metrics(self, query: str, language: str, results_count: int, response_time: float):
        """Log vector retrieval performance"""
        logger.info(
            f"VectorSearch - Query: {query[:50]}... | "
            f"Language: {language} | "
            f"Results: {results_count} | "
            f"Time: {response_time:.2f}s"
        )
