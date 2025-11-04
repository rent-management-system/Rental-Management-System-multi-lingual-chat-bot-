import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_production_workflow():
    """End-to-end production workflow test"""
    
    # Test 1: Knowledge base initialization
    response = client.get("/knowledge/stats")
    assert response.status_code == 200
    assert response.json()["kb_initialized"] == True
    
    # Test 2: Multilingual chat with knowledge boundaries
    responses = {}
    for lang in ["english", "amharic", "afan_oromo"]:
        response = client.post("/api/chat", json={
            "message": "How does pay-per-post work?",
            "language": lang
        })
        assert response.status_code == 200
        responses[lang] = response.json()
        assert "pay" in responses[lang]["response"].lower() or "ክፍያ" in responses[lang]["response"] or "kafalchi" in responses[lang]["response"].lower()
    
    # Test 3: Out-of-domain query handling
    response = client.post("/api/chat", json={
        "message": "What's the capital of France?",
        "language": "english"
    })
    assert response.status_code == 200
    assert "don't have information" in response.json()["response"].lower()
    
    # Test 4: Session persistence
    response = client.post("/api/chat", json={
        "message": "Hello", 
        "language": "english"
    })
    assert response.status_code == 200
    session_id = response.json()["session_id"]
    
    response = client.post("/api/chat", json={
        "message": "What was my previous question?",
        "session_id": session_id,
        "language": "english"
    })
    assert response.status_code == 200
    assert session_id == response.json()["session_id"]
