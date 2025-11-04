import logging
import time
from typing import Optional, Dict, Any
from app.services.vector_service import CachedVectorService
from app.services.translation_service import TranslationService
from app.services.ai_service import AIService
from app.services.session_service import SessionService
from app.workflows.chat_workflow import ChatWorkflow
from app.workflows.state import ChatState

# Configure logging
logger = logging.getLogger("chatbot_engine")

class ChatbotEngine:
    def __init__(self):
        """Initialize the chatbot engine with required services."""
        try:
            self.vector_service = CachedVectorService()
            self.translation_service = TranslationService()
            self.ai_service = AIService()
            self.session_service = SessionService()
            self.chat_workflow = ChatWorkflow(self.vector_service, self.ai_service)
            self.initialized = False
            self.query_count = 0
            self.error_count = 0
            self.total_response_time = 0
            
            # System prompts for different languages
            self.system_prompts = {
                "english": """CRITICAL: Answer ONLY from the provided knowledge base. If information is not in context, respond: "I don't have information about that in my knowledge base." NEVER invent, hallucinate, or provide information outside the rental management domain.""",
                "amharic": """CRITICAL: Answer ONLY from the provided knowledge base. If information is not in context, respond: "ስለዚህ በእውቀት መሠረቴ መረጃ የለኝም" NEVER invent, hallucinate, or provide information outside the rental management domain.""",
                "afan_oromo": """CRITICAL: Answer ONLY from the provided knowledge base. If information is not in context, respond: "Ani odeeffannoo kanaaf beerkuma koo keessatti hin qabu" NEVER invent, hallucinate, or provide information outside the rental management domain."""
            }
            
            logger.info("ChatbotEngine initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize ChatbotEngine: {str(e)}")
            raise

    async def initialize(self) -> bool:
        """Initialize the chatbot and its dependencies.
        
        Returns:
            bool: True if initialization was successful, False otherwise
        """
        try:
            logger.info("Initializing ChatbotEngine...")
            await self.vector_service.initialize_knowledge_base()
            self.initialized = True
            logger.info("ChatbotEngine initialization completed successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize ChatbotEngine: {str(e)}")
            self.initialized = False
            return False

    async def process_message(self, message: str, language: Optional[str] = None, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Process a user message and generate a response.
        
        Args:
            message: The user's message
            language: The language of the message (english, amharic, afan_oromo)
            session_id: Optional session ID for conversation tracking
            
        Returns:
            Dict containing the response and metadata
        """
        try:
            start_time = time.time()
            self.query_count += 1
            # Validate input
            if not message or not message.strip():
                raise ValueError("Empty message received")
            
            # Language detection
            if language is None:
                language = self._detect_language(message)
            
            language = language.lower()
            if language not in self.system_prompts:
                logger.warning(f"Unsupported language: {language}, defaulting to English")
                language = "english"
            
            # Get system prompt for the specified language
            system_prompt = self.system_prompts[language]
            
            # Get or create session
            session_state = self.session_service.get_session(session_id) if session_id else {}

            # Create chat state
            chat_state = ChatState(
                user_message=message,
                current_language=language,
                system_prompt=system_prompt,
                history=session_state.get('history', [])
            )

            # Execute workflow
            final_state = await self.chat_workflow.execute(chat_state)

            # Update session
            if session_id:
                self.session_service.update_session(session_id, final_state.to_dict())

            # Return successful response
            response_time = time.time() - start_time
            self.total_response_time += response_time
            return {
                "response": final_state.response,
                "language": final_state.current_language,
                "session_id": session_id,
                "status": "success"
            }
                
        except Exception as e:
            self.error_count += 1
            logger.critical(f"Critical error in process_message: {str(e)}", exc_info=True)
            # Default error response
            return {
                "response": {
                    "english": "I'm sorry, I'm having trouble processing your request. Please try again later.",
                    "amharic": "ይቅርታ፣ ጥያቄዎን ለማሰስ ችግር አጋጥሞኛል። እባክዎ ቆይተው ይሞክሩ።",
                    "afan_oromo": "Dhiifama, rakkoo ka'e jira. Yeroo booda irra deebi'ii yaalaa."
                }.get(language, "I'm sorry, I'm having trouble processing your request. Please try again later."),
                "language": language,
                "session_id": session_id,
                "status": "error"
            }

    def get_query_count(self) -> int:
        return self.query_count

    def get_error_rate(self) -> float:
        if self.query_count == 0:
            return 0.0
        return self.error_count / self.query_count

    def get_avg_response_time(self) -> float:
        if self.query_count == 0:
            return 0.0
        return self.total_response_time / self.query_count

    def _detect_language(self, message: str) -> str:
        # This is a placeholder for a more sophisticated language detection mechanism.
        # For now, we will just default to English.
        return "english"
