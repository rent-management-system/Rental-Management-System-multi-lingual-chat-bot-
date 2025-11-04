from datetime import datetime
from app.workflows.state import ChatState
from app.workflows.nodes.rag_retriever import RagRetrieverNode
from app.workflows.nodes.response_generator import ResponseGeneratorNode
from app.workflows.nodes.role_analyzer import RoleAnalyzerNode
from app.workflows.nodes.query_decomposition import QueryDecompositionNode
from app.workflows.nodes.memory_updater import MemoryUpdaterNode
from app.services.vector_service import VectorDatabaseService
from app.services.ai_service import AIService

class ChatWorkflow:
    def __init__(self, vector_service: VectorDatabaseService, ai_service: AIService):
        self.role_analyzer = RoleAnalyzerNode()
        self.query_decomposer = QueryDecompositionNode(ai_service)
        self.vector_retriever = RagRetrieverNode(vector_service)
        self.response_generator = ResponseGeneratorNode(ai_service)
        self.memory_updater = MemoryUpdaterNode()
    
    async def execute(self, state: ChatState) -> ChatState:
        state.metadata["timestamp"] = datetime.utcnow().isoformat()

        state = await self.role_analyzer.analyze_role(state)
        state = await self.query_decomposer.decompose_query(state)
        state = await self.vector_retriever.retrieve_context(state)
        state = await self.response_generator.generate_response(state)
        state = await self.memory_updater.update_memory(state)
        return state
