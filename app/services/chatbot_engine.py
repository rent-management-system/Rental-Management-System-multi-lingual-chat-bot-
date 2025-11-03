from typing import Optional
from app.services.vector_service import CachedVectorService
from app.services.translation_service import TranslationService

class ChatbotEngine:
    def __init__(self):
        self.vector_service = CachedVectorService()
        self.translation_service = TranslationService()

    async def process_message(self, message: str, language: str, session_id: Optional[str] = None) -> dict:
        # Use vector similarity search to get context
        relevant_contexts = await self.vector_service.similarity_search(message, language)

        # Compose response (mocked for now)
        response_text = f"Response based on context: {relevant_contexts[0] if relevant_contexts else 'No relevant info found.'}"

        # Return structured response
        return {
            "response": response_text,
            "language": language,
            "session_id": session_id
        }
