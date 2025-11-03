from app.workflows.state import ChatState
from app.workflows.nodes.vector_retriever import VectorRetrieverNode

class ChatWorkflow:
    def __init__(self):
        self.vector_retriever = VectorRetrieverNode()
    
    async def run(self, user_message: str, language: str) -> ChatState:
        state = ChatState(user_message=user_message, current_language=language)
        state = await self.vector_retriever.retrieve_context(state)
        return state
