import logging
from typing import Literal, Dict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Language mapping for Gemini
LANGUAGE_MAP: Dict[Literal["english", "amharic", "afaan_oromo"], str] = {
    "english": "English",
    "amharic": "Amharic",
    "afaan_oromo": "Afaan Oromo",
}

def get_gemini_language_code(lang: Literal["english", "amharic", "afaan_oromo"]) -> str:
    """Maps internal language codes to Gemini-compatible language names."""
    return LANGUAGE_MAP.get(lang, "English") # Default to English if somehow an invalid lang gets through
