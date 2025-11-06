from fastapi.testclient import TestClient
from app.main import app
from app.vector_store import faiss_vector_store
from unittest.mock import patch, MagicMock
import pytest

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def mock_faiss_init():
    """
    Mocks FAISS initialization to prevent actual model loading during tests.
    Ensures faiss_vector_store._index is set to a mock object.
    """
    with patch('app.vector_store.FAISSVectorStore._initialize_store') as mock_init:
        # Simulate successful initialization by setting a mock index
        faiss_vector_store._index = MagicMock()
        faiss_vector_store._documents = ["doc1", "doc2", "doc3"]
        yield
        # Clean up after tests if necessary
        faiss_vector_store._index = None
        faiss_vector_store._documents = []


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@patch('app.chatbot_graph.chatbot_graph.invoke')
def test_chat_english_success(mock_invoke):
    mock_invoke.return_value = {"response": "This is an English response."}
    response = client.post("/chat", json={"query": "Hello", "language": "english"})
    assert response.status_code == 200
    assert response.json() == {"response": "This is an English response."}
    mock_invoke.assert_called_once_with({'query': 'Hello', 'language': 'english', 'context': [], 'response': ''})

@patch('app.chatbot_graph.chatbot_graph.invoke')
def test_chat_amharic_success(mock_invoke):
    mock_invoke.return_value = {"response": "ይህ የአማርኛ ምላሽ ነው።"}
    response = client.post("/chat", json={"query": "ሰላም", "language": "amharic"})
    assert response.status_code == 200
    assert response.json() == {"response": "ይህ የአማርኛ ምላሽ ነው።"}
    mock_invoke.assert_called_once_with({'query': 'ሰላም', 'language': 'amharic', 'context': [], 'response': ''})

@patch('app.chatbot_graph.chatbot_graph.invoke')
def test_chat_afaan_oromo_success(mock_invoke):
    mock_invoke.return_value = {"response": "Kun deebii Afaan Oromooti."}
    response = client.post("/chat", json={"query": "Akkam", "language": "afaan_oromo"})
    assert response.status_code == 200
    assert response.json() == {"response": "Kun deebii Afaan Oromooti."}
    mock_invoke.assert_called_once_with({'query': 'Akkam', 'language': 'afaan_oromo', 'context': [], 'response': ''})

@patch('app.chatbot_graph.chatbot_graph.invoke')
def test_chat_auto_detect_success(mock_invoke):
    mock_invoke.return_value = {"response": "This is an auto-detected response."}
    response = client.post("/chat", json={"query": "Hello"})
    assert response.status_code == 200
    assert response.json() == {"response": "This is an auto-detected response."}
    mock_invoke.assert_called_once_with({'query': 'Hello', 'language': 'english', 'context': [], 'response': ''}) # Default to english

def test_chat_empty_query():
    response = client.post("/chat", json={"query": ""})
    assert response.status_code == 422 # Pydantic validation error

def test_chat_invalid_language():
    response = client.post("/chat", json={"query": "Hello", "language": "klingon"})
    assert response.status_code == 422 # Pydantic validation error

@patch('app.chatbot_graph.chatbot_graph.invoke')
def test_chat_llm_failure(mock_invoke):
    mock_invoke.return_value = {"response": "Sorry, I encountered an issue while generating a response. Please try rephrasing your question."}
    response = client.post("/chat", json={"query": "Test failure"})
    assert response.status_code == 500
    assert "Sorry, I encountered an issue" in response.json()["detail"]

@patch('app.vector_store.faiss_vector_store._index', None) # Simulate FAISS not initialized
def test_chat_faiss_not_ready():
    response = client.post("/chat", json={"query": "Hello"})
    assert response.status_code == 500
    assert "Chatbot service is not ready" in response.json()["detail"]
