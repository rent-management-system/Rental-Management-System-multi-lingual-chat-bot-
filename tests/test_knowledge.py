from app.knowledge_base import load_and_split_documents, MultilingualEmbeddings
import pytest
import os

def test_load_and_split_documents():
    chunks = load_and_split_documents()
    assert isinstance(chunks, list)
    assert len(chunks) > 0
    assert isinstance(chunks[0], str)
    # Check chunk size and overlap roughly
    assert len(chunks[0]) <= 500
    assert len(chunks[1]) <= 500

def test_embedding_model_singleton():
    model1 = MultilingualEmbeddings.get_embedding_model()
    model2 = MultilingualEmbeddings.get_embedding_model()
    assert model1 is model2 # Ensure it's a singleton

def test_embedding_model_embed_documents():
    texts = ["hello world", "this is a test", "another sentence"]
    embeddings = MultilingualEmbeddings().embed_documents(texts)
    assert isinstance(embeddings, list)
    assert len(embeddings) == len(texts)
    assert isinstance(embeddings[0], list)
    assert len(embeddings[0]) > 0 # Check if embeddings are generated

def test_embedding_model_embed_query():
    query = "test query"
    embedding = MultilingualEmbeddings().embed_query(query)
    assert isinstance(embedding, list)
    assert len(embedding) > 0 # Check if embedding is generated
