from typing import Optional, Dict

class ChatState:
    def __init__(self, user_message: str, current_language: str):
        self.user_message = user_message
        self.current_language = current_language
        self.context: Optional[str] = None
        self.metadata: Dict[str, any] = {}
