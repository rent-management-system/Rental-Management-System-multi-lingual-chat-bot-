from typing import List
from app.services.vector_service import VectorDatabaseService
from app.services.translation_service import TranslationService
from app.workflows.state import ChatState

class VectorRetrieverNode:
    def __init__(self):
        self.vector_service = VectorDatabaseService()
        self.translation_service = TranslationService()
    
    async def retrieve_context(self, state: ChatState):
        # Use language-specific embedding enhancement
        enhanced_query = self._add_language_context(state.user_message, state.current_language)
        return await self.vector_service.similarity_search(enhanced_query, state.current_language)

    def _add_language_context(self, query: str, language: str) -> str:
        # This is a placeholder for a more sophisticated language-specific query enhancement.
        # For now, we just prepend the language to the query.
        return f"{language}: {query}"
    
    def _enhance_query(self, query: str, language: str) -> str:
        """Enhance query with domain-specific terms"""
        domain_terms = {
            "amharic": ["", "", "", "", ""],
            "english": ["rental", "property", "landlord", "tenant", "management"],
            "afan_oromo": ["kiraa", "mana", "abbootii manaa", "kireeffata", "bulchiinsa"]
        }
        
        terms = domain_terms.get(language, domain_terms["english"])
        enhanced = f"{query} {' '.join(terms)}"
        return enhanced
    
    def _format_context(self, documents: List[str], language: str) -> str:
        """Format retrieved documents into context"""
        context_header = {
            "english": "RELEVANT SYSTEM INFORMATION:",
            "amharic": "",
            "afan_oromo": "Odeeffannoo Sirnaa Irraa Argame:"
        }
        
        formatted_docs = "\n\n".join([f" {doc}" for doc in documents])
        return f"{context_header.get(language, context_header['english'])}\n\n{formatted_docs}"
