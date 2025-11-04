import json
from typing import Optional, Dict, Any

class TranslationService:
    def __init__(self):
        self.translations = self._load_translations()
        self.language_stats: Dict[str, int] = {"english": 0, "amharic": 0, "afan_oromo": 0}
    
    def _load_translations(self) -> dict:
        # Load translations from knowledge_base/translations/translation.json
        try:
            with open("./knowledge_base/translations/translation.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def translate(self, text: str, target_language: str) -> Optional[str]:
        # Simple key-based translation lookup (can be extended)
        lang_data = self.translations.get(target_language, {})
        return lang_data.get(text, None)

    def record_language_usage(self, language: str):
        self.language_stats[language] = self.language_stats.get(language, 0) + 1

    def get_language_stats(self) -> Dict[str, int]:
        return self.language_stats
