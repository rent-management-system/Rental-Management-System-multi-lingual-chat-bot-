from app.chatbot_graph import retrieve, generate, ChatbotState, chatbot_graph
from app.vector_store import faiss_vector_store
from unittest.mock import patch, MagicMock
import pytest
from typing import Dict, Any

@pytest.fixture
def mock_faiss_search():
    with patch('app.vector_store.FAISSVectorStore.search') as mock_search:
        mock_search.return_value = ["context chunk 1", "context chunk 2"]
        yield mock_search

@pytest.fixture
def mock_llm_invoke():
    with patch('app.chatbot_graph.llm.invoke') as mock_invoke:
        mock_invoke.return_value = MagicMock(content="Mocked LLM response")
        yield mock_invoke

def test_retrieve_node(mock_faiss_search):
    state = ChatbotState(query="test query", language="english")
    result = retrieve(state)
    assert "context" in result
    assert result["context"] == ["context chunk 1", "context chunk 2"]
    mock_faiss_search.assert_called_once_with("test query", k=3)

def test_generate_node_success(mock_llm_invoke):
    state = ChatbotState(query="test query", language="english", context=["context chunk 1"])
    result = generate(state)
    assert "response" in result
    assert result["response"] == "Mocked LLM response"
    mock_llm_invoke.assert_called_once()

def test_generate_node_llm_failure(mock_llm_invoke):
    mock_llm_invoke.side_effect = Exception("LLM API error")
    state = ChatbotState(query="test query", language="english", context=["context chunk 1"])
    result = generate(state)
    assert "response" in result
    assert "Sorry, I encountered an issue" in result["response"]

@patch('app.vector_store.FAISSVectorStore.search', return_value=["graph context 1"])
@patch('app.chatbot_graph.llm.invoke', return_value=MagicMock(content="Graph test response"))
def test_chatbot_graph_end_to_end(mock_llm, mock_faiss):
    # Ensure FAISS is initialized for the graph to run
    _ = faiss_vector_store
    
    initial_state = ChatbotState(query="graph query", language="english")
    result = chatbot_graph.invoke(initial_state)
    
    assert "response" in result
    assert result["response"] == "Graph test response"
    mock_faiss.assert_called_once_with("graph query", k=3)
    mock_llm.assert_called_once()
