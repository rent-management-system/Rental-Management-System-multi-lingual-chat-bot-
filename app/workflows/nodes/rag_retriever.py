from typing import List, Dict, Any
from app.services.vector_service import VectorDatabaseService
from app.workflows.state import ChatState
from langchain_core.documents import Document

class RagRetrieverNode:
    def __init__(self, vector_service: VectorDatabaseService):
        self.vector_service = vector_service
    
    async def retrieve_context(self, state: ChatState) -> ChatState:
        all_relevant_docs: List[Document] = []
        sub_queries = state.metadata.get("sub_queries", [state.user_message])
        metadata_filters = state.metadata.get("filters", {}) # Placeholder for future metadata filtering

        for query in sub_queries:
            # Enhance query with language context if needed (though query decomposition should handle this)
            enhanced_query = self._enhance_query(query, state.current_language)
            
            # Perform similarity search
            # In a real scenario, metadata_filters would be passed to similarity_search
            results = await self.vector_service.similarity_search(enhanced_query, state.current_language)
            
            # Extract documents from results and add to all_relevant_docs
            for res in results:
                # Assuming res["document"] is already a Document object or can be converted
                if isinstance(res["document"], Document):
                    all_relevant_docs.append(res["document"])
                else:
                    # Fallback if it's just page_content
                    all_relevant_docs.append(Document(page_content=res["document"], metadata=res.get("metadata", {})))

        # Deduplicate documents if necessary (e.g., by page_content or a unique ID in metadata)
        unique_docs = []
        seen_content = set()
        for doc in all_relevant_docs:
            if doc.page_content not in seen_content:
                unique_docs.append(doc)
                seen_content.add(doc.page_content)

        # Format the retrieved documents into context
        state.context = self._format_context(unique_docs, state.current_language)
        return state

    def _enhance_query(self, query: str, language: str) -> str:
        """Enhance query with domain-specific terms based on language."""
        domain_terms = {
            "amharic": ["ኪራይ", "ንብረት", "ባለቤት", "ተከራይ", "አስተዳደር"],
            "english": ["rental", "property", "landlord", "tenant", "management"],
            "afan_oromo": ["kiraa", "mana", "abbootii manaa", "kireeffata", "bulchiinsa"]
        }
        
        terms = domain_terms.get(language, domain_terms["english"])
        # Simple enhancement: append relevant terms. More advanced would use LLM.
        enhanced = f"{query} {' '.join(terms)}"
        return enhanced
    
    def _format_context(self, documents: List[Document], language: str) -> str:
        """Format retrieved Document objects into a single context string."""
        context_header = {
            "english": "RELEVANT SYSTEM INFORMATION:",
            "amharic": "ተዛማጅ የስርዓት መረጃ:",
            "afan_oromo": "Odeeffannoo Sirnaa Irraa Argame:"
        }
        
        formatted_docs = "\n\n".join([f"- {doc.page_content}" for doc in documents])
        return f"{context_header.get(language, context_header['english'])}\n\n{formatted_docs}"
