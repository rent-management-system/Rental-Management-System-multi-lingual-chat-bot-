import json
from typing import List
import docx

class KnowledgeLoader:
    def __init__(self):
        self.knowledge_path = "./knowledge_base"

    async def load_all_documents(self) -> List[str]:
        """Load all knowledge base documents"""
        documents = []

        # 1. Load project documentation
        docx_content = self._process_docx(f"{self.knowledge_path}/Final project 1-4 final.docx")
        documents.append(f"PROJECT_DOCS:\n{docx_content}")

        # 2. Load translation files as context
        translations = self._load_translation_context()
        documents.append(f"TRANSLATIONS:\n{translations}")

        # 3. Load FAQ knowledge
        faqs = self._load_faqs()
        documents.extend(faqs)

        return documents

    def _process_docx(self, file_path: str) -> str:
        """Process a .docx file and return its text content."""
        try:
            doc = docx.Document(file_path)
            full_text = []
            for para in doc.paragraphs:
                full_text.append(para.text)
            return '\n'.join(full_text)
        except Exception as e:
            print(f"Error processing docx file: {e}")
            return ""

    def _load_translation_context(self) -> str:
        """Load all translation files as searchable context"""
        try:
            with open(f"{self.knowledge_path}/translations/translation.json", 'r', encoding='utf-8') as f:
                translations = json.load(f)
            return json.dumps(translations, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error loading translation file: {e}")
            return ""

    def _load_faqs(self) -> List[str]:
        """Load FAQ documents"""
        try:
            with open(f"{self.knowledge_path}/faqs/Faq.txt", 'r', encoding='utf-8') as f:
                faqs = f.read()
            return [faqs]
        except Exception as e:
            print(f"Error loading faq file: {e}")
            return []
