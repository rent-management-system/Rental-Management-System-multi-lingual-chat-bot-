import pytest
import asyncio
from app.services.knowledge_loader import KnowledgeLoader

@pytest.mark.asyncio
async def test_load_all_documents():
    loader = KnowledgeLoader()
    documents = await loader.load_all_documents()
    
    assert documents
    assert any("PROJECT_DOCS" in doc for doc in documents)
    assert any("TRANSLATIONS" in doc for doc in documents)
    assert any("FREQUENTLY ASKED QUESTIONS" in doc for doc in documents)

@pytest.mark.asyncio
async def test_load_project_documentation():
    loader = KnowledgeLoader()
    project_doc = loader._load_project_documentation()
    assert "RENTAL MANAGEMENT SYSTEM" in project_doc

@pytest.mark.asyncio
async def test_load_translations_context():
    loader = KnowledgeLoader()
    translations = loader._load_translations_context()
    assert "amharic" in translations
    assert "english" in translations
    assert "afan_oromo" in translations

@pytest.mark.asyncio
async def test_load_faqs():
    loader = KnowledgeLoader()
    faqs = loader._load_faqs()
    assert faqs
    assert any("How do I list my property" in faq for faq in faqs)
