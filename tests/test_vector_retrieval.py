import pytest
import asyncio
from app.services.vector_service import VectorDatabaseService
from app.services.embedding_service import LocalEmbeddingService
from sklearn.metrics.pairwise import cosine_similarity

@pytest.mark.asyncio
async def test_vector_similarity_search():
    """Test vector DB retrieval accuracy"""
    vector_service = VectorDatabaseService()
    
    # Test English query
    english_results = await vector_service.similarity_search(
        "How to list property as landlord?", "english"
    )
    assert len(english_results) > 0
    assert any("pay-per-post" in doc.lower() for doc in english_results)
    
    # Test Amharic query
    amharic_results = await vector_service.similarity_search(
        "ንብረት እንዴት ማስተዳደር?", "amharic"
    )
    assert len(amharic_results) > 0
    
    # Test Afan Oromo query  
    oromo_results = await vector_service.similarity_search(
        "Akkaataa mana kiraa", "afan_oromo"
    )
    assert len(oromo_results) > 0

@pytest.mark.asyncio
async def test_embedding_quality():
    """Test embedding generation and similarity"""
    embedding_service = LocalEmbeddingService()
    
    # Test similar concepts have similar embeddings
    emb1 = await embedding_service.embed_text("rental property")
    emb2 = await embedding_service.embed_text("house for rent")
    
    similarity = cosine_similarity([emb1], [emb2])[0][0]
    assert similarity > 0.7  # Should be semantically similar
