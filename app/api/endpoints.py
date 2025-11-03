from fastapi import APIRouter, Depends, BackgroundTasks, Query, Header
from typing import Optional
from app.models.user_models import User
from app.models.chat_models import ChatRequest, ChatResponse
from app.services.vector_service import VectorDatabaseService
from app.services.chatbot_engine import ChatbotEngine
from app.services.translation_service import TranslationService
from app.api.dependencies import get_current_user, get_admin_user

router = APIRouter()

vector_service = VectorDatabaseService()
chatbot_engine = ChatbotEngine()
translation_service = TranslationService()

@router.post("/chat", response_model=ChatResponse)
async def chat_with_bot(
    request: ChatRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    language: Optional[str] = Query(None),
    x_language: Optional[str] = Header(None, alias="X-Language")
):
    """
    Chat with AI assistant using Vector DB knowledge retrieval
    
    **Vector Search Features:**
    - Semantic similarity matching across all documents
    - Multi-lingual embedding support
    - Context-aware response generation
    - Real-time knowledge retrieval
    
    **Examples:**
    ```json
    {
      "message": "How does pay-per-post work?",
      "language": "english"
    }
    ```
    """
    final_language = (language or x_language or 
                     request.language or 
                     await detect_language_from_text(request.message))
    
    return await chatbot_engine.process_message(
        message=request.message,
        language=final_language,
        session_id=request.session_id
    )

@router.post("/knowledge/refresh")
async def refresh_knowledge_base(
    current_user: User = Depends(get_admin_user)
):
    """
    Refresh vector database with latest knowledge base
    (Admin only - for updating knowledge content)
    """
    await vector_service.initialize_knowledge_base()
    return {"status": "success", "message": "Knowledge base refreshed"}

@router.get("/knowledge/stats")
async def get_knowledge_stats(
    current_user: User = Depends(get_current_user)
):
    """Get vector database statistics"""
    stats = await vector_service.get_collection_stats()
    return {"vector_db_stats": stats}
