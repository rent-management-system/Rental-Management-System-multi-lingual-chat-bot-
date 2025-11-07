import os
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from app.api.endpoints import router
from app.services.knowledge_loader import KnowledgeLoader
from app.services.vector_service import VectorDatabaseService
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Verify required environment variables
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY environment variable is not set")

app = FastAPI(
    title="Ethiopian Rental Management Chatbot",
    description="Multilingual chatbot with vector DB and Gemini embeddings",
    version="1.0.0"
)

# Add security and performance middleware
@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    return response

app.add_middleware(GZipMiddleware, minimum_size=1000)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize vector database on startup
vector_service = VectorDatabaseService()
knowledge_loader = KnowledgeLoader()

@app.on_event("startup")
async def startup_event():
    if not vector_service.is_initialized():
        await knowledge_loader.load_all_documents()
        await vector_service.initialize_knowledge_base()

from datetime import datetime
import psutil
from app.services.ai_service import AIService

# Load environment variables
load_dotenv()

# Verify required environment variables
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY environment variable is not set")

app = FastAPI(
    title="Multilingual Chatbot API",
    description="Backend for a multilingual chatbot using FastAPI, LangGraph, Gemini, and FAISS.",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Initialize services
vector_service = VectorDatabaseService()
knowledge_loader = KnowledgeLoader()
ai_service = AIService()


@app.on_event("startup")
async def startup_event():
    logger.info("Application startup: Initializing FAISS vector store (if not already).")
    # Accessing faiss_vector_store instance triggers its lazy initialization
    # This ensures the model is loaded and index built on startup,
    # but only if the first request hasn't already done so.
    _ = faiss_vector_store
    if faiss_vector_store._index is None:
        logger.error("FAISS vector store failed to initialize during startup.")
    else:
        logger.info("FAISS vector store ready.")

@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check endpoint.
    """
    # Check if the vector store is initialized as part of the health check
    if faiss_vector_store.get_index() is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Chatbot service is not ready. FAISS index not initialized.",
        )
    return {"status": "ok"}

@app.post("/chat", status_code=status.HTTP_200_OK)
async def chat_endpoint(request: ChatRequest):
    """
    Processes a user query and returns a multilingual response from the chatbot.
    """
    logger.info(f"Received chat request: Query='{request.query}', Language='{request.language}'")



@app.get("/metrics")
async def application_metrics():
    return {
        "active_sessions": chat_engine.session_service.get_active_count(),
        "total_queries": chat_engine.get_query_count(),
        "language_distribution": chat_engine.translation_service.get_language_stats(),
        "average_response_time": chat_engine.get_avg_response_time(),
        "error_rate": chat_engine.get_error_rate()
    }

    if not faiss_vector_store._index:
        logger.error("FAISS index not available. Returning 500 error.")

    # The get_index() method will handle initialization if needed.
    if faiss_vector_store.get_index() is None:
        logger.error("FAISS index not available after attempting initialization. Returning 500 error.")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Chatbot service is not ready. Please try again later."
        )

    try:
        # LangGraph expects a dictionary for initial state
        initial_state = ChatbotState(query=request.query, language=request.language or "english")
        
        # Invoke the chatbot graph
        result = chatbot_graph.invoke(initial_state)
        
        response_text = result.get("response", "Sorry, I couldn't generate a response.")
        
        if "Sorry, I encountered an issue" in response_text:
            logger.error(f"LLM generation failed for query: '{request.query}'")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=response_text
            )

        logger.info(f"Chat response generated for query: '{request.query}'")
        return {"response": response_text}
    except HTTPException:
        raise # Re-raise HTTPExceptions
    except Exception as e:
        logger.error(f"An unexpected error occurred during chat processing: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again."
        )


        