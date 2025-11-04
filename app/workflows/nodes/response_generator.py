from app.workflows.state import ChatState
from app.services.ai_service import AIService

class ResponseGeneratorNode:
    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service

    async def generate_response(self, state: ChatState) -> ChatState:
        prompt = f"{state.system_prompt}\n\nContext:\n{state.context}\n\nUser Question: {state.user_message}\n\nResponse:"
        response_text = await self.ai_service.generate_response(prompt)
        state.response = response_text
        return state

