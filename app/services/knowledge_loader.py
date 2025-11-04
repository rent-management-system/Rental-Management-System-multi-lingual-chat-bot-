import json
from typing import List
import docx
from langchain_core.documents import Document
from app.services.chunker import ChunkerService

class KnowledgeLoader:
    def __init__(self):
        self.knowledge_path = "./knowledge_base"
        self.chunker = ChunkerService() # Initialize the chunker

    async def load_all_documents(self) -> List[Document]:
        """Load all knowledge base documents, chunk them, and return as Document objects."""
        all_documents: List[Document] = []

        # 1. Load project documentation (DOCX)
        docx_content = self._process_docx(f"{self.knowledge_path}/Final project 1-4 final.docx")
        if docx_content:
            all_documents.extend(self.chunker.chunk_text(docx_content, metadata={"source": "Final project 1-4 final.docx", "type": "project_documentation"}))

        # 2. Load translation files as context
        translation_content = self._load_translation_context()
        if translation_content:
            all_documents.extend(self.chunker.chunk_text(translation_content, metadata={"source": "translation.json", "type": "translation_context"}))

        # 3. Load FAQ knowledge (TXT)
        faq_content = self._load_faqs()
        if faq_content:
            all_documents.extend(self.chunker.chunk_text(faq_content, metadata={"source": "Faq.txt", "type": "faq"}))

        return all_documents

    def _process_docx(self, file_path: str) -> str:
        """Process a .docx file and return its text content."""
        try:
            doc = docx.Document(file_path)
            full_text = []
            for para in doc.paragraphs:
                full_text.append(para.text)
            return '\n'.join(full_text)
        except Exception as e:
            print(f"Error processing docx file {file_path}: {e}")
            return ""

    def _load_translation_context(self) -> str:
        """Load all translation files as searchable context"""
        try:
            with open(f"{self.knowledge_path}/translations/translation.json", 'r', encoding='utf-8') as f:
                translations = json.load(f)
            return json.dumps(translations, ensure_ascii=False, indent=2)
        except FileNotFoundError:
            print(f"Translation file not found: {self.knowledge_path}/translations/translation.json")
            return ""
        except Exception as e:
            print(f"Error loading translation file: {e}")
            return ""

    def _load_faqs(self) -> str:
        """Load FAQ documents"""
        try:
            with open(f"{self.knowledge_path}/faqs/Faq.txt", 'r', encoding='utf-8') as f:
                faqs = f.read()
            return faqs
        except FileNotFoundError:
            print(f"FAQ file not found: {self.knowledge_path}/faqs/Faq.txt")
            return ""
        except Exception as e:
            print(f"Error loading faq file: {e}")
            return ""
