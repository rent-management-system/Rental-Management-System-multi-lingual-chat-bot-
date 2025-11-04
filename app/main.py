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

# Initialize services
vector_service = VectorDatabaseService()
knowledge_loader = KnowledgeLoader()
ai_service = AIService()

@app.on_event("startup")
async def startup_event():
    if not vector_service.is_initialized():
        await knowledge_loader.load_all_documents()
        await vector_service.initialize_knowledge_base()

app.include_router(router, prefix="/api")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "vector_db": vector_service.get_status(),
        "ai_service": ai_service.get_status(),
        "memory_usage": f"{psutil.Process().memory_info().rss / 1024 / 1024:.2f} MB"
    }

@app.get("/knowledge/stats")
async def knowledge_stats():
    return {
        "vector_docs": vector_service.get_document_count(),
        "languages_supported": ["amharic", "english", "afan_oromo"],
        "kb_initialized": vector_service.is_initialized()
    }


@app.get("/metrics")
async def application_metrics():
    return {
        "active_sessions": chat_engine.session_service.get_active_count(),
        "total_queries": chat_engine.get_query_count(),
        "language_distribution": chat_engine.translation_service.get_language_stats(),
        "average_response_time": chat_engine.get_avg_response_time(),
        "error_rate": chat_engine.get_error_rate()
    }