from typing import Dict, Any, Optional

class SessionService:
    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}

    def get_active_count(self) -> int:
        """Get the number of active sessions."""
        return len(self.sessions)

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        return self.sessions.get(session_id)

    def update_session(self, session_id: str, state: Dict[str, Any]):
        if session_id not in self.sessions:
            self.sessions[session_id] = {}
        self.sessions[session_id].update(state)
