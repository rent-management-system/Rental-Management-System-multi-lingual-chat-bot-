from typing import List
from app.workflows.state import ChatState
from app.services.ai_service import AIService

class QueryDecompositionNode:
    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service

    async def decompose_query(self, state: ChatState) -> ChatState:
        # This is a simplified example. A real decomposition would involve more sophisticated prompting.
        prompt = f"Decompose the following user query into 1-3 simpler, focused sub-queries. Return them as a comma-separated list.\nUser Query: {state.user_message}"
        
        try:
            decomposition_response = await self.ai_service.generate_response(prompt)
            sub_queries = [q.strip() for q in decomposition_response.split(',') if q.strip()]
            if not sub_queries:
                sub_queries = [state.user_message] # Fallback to original query
        except Exception as e:
            print(f"Error during query decomposition: {e}")
            sub_queries = [state.user_message] # Fallback to original query

        state.metadata["sub_queries"] = sub_queries
        return state
