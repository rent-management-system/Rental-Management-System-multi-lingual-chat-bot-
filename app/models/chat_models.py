from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    message: str
    language: Optional[str] = None
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    language: Optional[str] = None
    session_id: Optional[str] = None
