from typing import Dict, Any
from app.workflows.state import ChatState

class RoleAnalyzerNode:
    def __init__(self):
        # Define keywords for role inference
        self.recruiter_keywords = ["recruiter", "hiring manager", "job offer", "interview"]
        self.visitor_keywords = ["visitor", "guest", "tour", "information"]

    async def analyze_role(self, state: ChatState) -> ChatState:
        user_message = state.user_message.lower()
        inferred_role = "general_user"

        if any(keyword in user_message for keyword in self.recruiter_keywords):
            inferred_role = "recruiter"
        elif any(keyword in user_message for keyword in self.visitor_keywords):
            inferred_role = "visitor"
        
        state.metadata["inferred_role"] = inferred_role
        return state
