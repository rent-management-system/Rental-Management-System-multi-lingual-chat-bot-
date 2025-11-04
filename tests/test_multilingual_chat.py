import pytest
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

@pytest.mark.asyncio
async def test_knowledge_boundaries():
    # Test that system doesn't hallucinate
    response = client.post("/api/chat", json={"message": "What's the weather?", "language": "english"})
    assert response.status_code == 200
    assert "don't have information" in response.json()["response"].lower()

@pytest.mark.asyncio
async def test_multilingual_consistency():
    # Test same question in all languages gets similar answers
    questions = {
        "english": "How to list property?",
        "amharic": "ንብረት እንዴት ማስተዳደር?",
        "afan_oromo": "Akkaataa mana sirreessuu?"
    }
    
    responses = []
    for lang, question in questions.items():
        response = client.post("/api/chat", json={"message": question, "language": lang})
        assert response.status_code == 200
        responses.append(response.json()["response"])
    
    # This is a simple check. A more sophisticated check would involve checking for semantic similarity.
    assert "pay-per-post" in responses[0].lower()
    assert "pay-per-post" in responses[1].lower()
    assert "pay-per-post" in responses[2].lower()
