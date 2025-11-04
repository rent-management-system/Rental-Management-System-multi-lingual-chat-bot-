from typing import List, Dict, Any
from app.workflows.state import ChatState
import json
import os

CHAT_HISTORY_FILE = "chat_history.jsonl"

class MemoryUpdaterNode:
    def __init__(self):
        self.chat_history_file = CHAT_HISTORY_FILE
        self._ensure_history_file_exists()

    def _ensure_history_file_exists(self):
        if not os.path.exists(self.chat_history_file):
            with open(self.chat_history_file, 'w') as f:
                pass # Create an empty file

    async def update_memory(self, state: ChatState) -> ChatState:
        # Update in-memory conversation history (keeping last 5 turns)
        if state.user_message and state.response:
            state.history.append({"role": "user", "content": state.user_message})
            state.history.append({"role": "ai", "content": state.response})
            state.history = state.history[-10:] # Keep last 5 turns (user + ai)

        # Log interaction to persistent file
        self._log_interaction(state)
        return state

    def _log_interaction(self, state: ChatState):
        log_entry = {
            "timestamp": state.metadata.get("timestamp"),
            "session_id": state.metadata.get("session_id"),
            "user_message": state.user_message,
            "inferred_role": state.metadata.get("inferred_role"),
            "sub_queries": state.metadata.get("sub_queries"),
            "retrieved_context": state.context,
            "ai_response": state.response,
            "language": state.current_language,
            "metadata": state.metadata # Include all metadata for comprehensive logging
        }
        with open(self.chat_history_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
