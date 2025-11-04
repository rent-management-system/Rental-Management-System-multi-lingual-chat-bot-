from typing import Optional, Dict, Any, List

class ChatState:
    def __init__(self, user_message: str, current_language: str, system_prompt: str, history: List[Dict[str, str]]):
        self.user_message = user_message
        self.current_language = current_language
        self.system_prompt = system_prompt
        self.history = history
        self.context: Optional[str] = None
        self.response: Optional[str] = None
        self.metadata: Dict[str, Any] = {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_message": self.user_message,
            "current_language": self.current_language,
            "system_prompt": self.system_prompt,
            "history": self.history,
            "context": self.context,
            "response": self.response,
            "metadata": self.metadata,
        }
