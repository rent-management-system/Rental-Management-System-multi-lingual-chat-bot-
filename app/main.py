import os
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from app.models import ChatRequest
from app.chatbot_graph import chatbot_graph, ChatbotState
from app.utils import logger
from app.vector_store import faiss_vector_store # Import to trigger lazy loading

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
    return {"status": "ok"}

@app.post("/chat", status_code=status.HTTP_200_OK)
async def chat_endpoint(request: ChatRequest):
    """
    Processes a user query and returns a multilingual response from the chatbot.
    """
    logger.info(f"Received chat request: Query='{request.query}', Language='{request.language}'")

    if not faiss_vector_store._index:
        logger.error("FAISS index not available. Returning 500 error.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Chatbot service is not ready. Please try again later."
        )

    try:
        # LangGraph expects a dictionary for initial state
        initial_state = ChatbotState(query=request.query, language=request.language or "english")
        
        # Invoke the chatbot graph
        # LangGraph's invoke method is synchronous by default,
        # but FastAPI handles it in an async context.
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
