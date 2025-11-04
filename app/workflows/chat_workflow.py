from app.workflows.state import ChatState
from app.workflows.nodes.vector_retriever import VectorRetrieverNode
from app.workflows.nodes.response_generator import ResponseGeneratorNode
from app.services.vector_service import VectorDatabaseService
from app.services.ai_service import AIService

class ChatWorkflow:
    def __init__(self, vector_service: VectorDatabaseService, ai_service: AIService):
        self.vector_retriever = VectorRetrieverNode(vector_service)
        self.response_generator = ResponseGeneratorNode(ai_service)
    
    async def execute(self, state: ChatState) -> ChatState:
        state = await self.vector_retriever.retrieve_context(state)
        state = await self.response_generator.generate_response(state)
        return state
