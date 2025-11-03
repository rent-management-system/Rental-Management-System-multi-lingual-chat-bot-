import json
from typing import Optional

class TranslationService:
    def __init__(self):
        self.translations = self._load_translations()
    
    def _load_translations(self) -> dict:
        # Load translations from knowledge_base/translations JSON files
        translations = {}
        for lang in ["amharic", "english", "afan_oromo"]:
            try:
                with open(f"./knowledge_base/translations/{lang}.json", "r", encoding="utf-8") as f:
                    translations[lang] = json.load(f)
            except FileNotFoundError:
                translations[lang] = {}
        return translations
    
    def translate(self, text: str, target_language: str) -> Optional[str]:
        # Simple key-based translation lookup (can be extended)
        lang_data = self.translations.get(target_language, {})
        return lang_data.get(text, None)
