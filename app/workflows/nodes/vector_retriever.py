from typing import List
from app.services.vector_service import VectorDatabaseService
from app.services.translation_service import TranslationService
from app.workflows.state import ChatState

class VectorRetrieverNode:
    def __init__(self):
        self.vector_service = VectorDatabaseService()
        self.translation_service = TranslationService()
    
    async def retrieve_context(self, state: ChatState) -> ChatState:
        """Enhanced context retrieval using vector similarity search"""
        
        # Prepare query for better retrieval
        enhanced_query = self._enhance_query(state.user_message, state.current_language)
        
        # Perform vector similarity search
        relevant_docs = await self.vector_service.similarity_search(
            query=enhanced_query,
            language=state.current_language,
            k=5  # Top 5 most relevant documents
        )
        
        # Combine and format context
        state.context = self._format_context(relevant_docs, state.current_language)
        state.metadata["retrieved_docs_count"] = len(relevant_docs)
        state.metadata["retrieval_method"] = "vector_similarity"
        
        return state
    
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
