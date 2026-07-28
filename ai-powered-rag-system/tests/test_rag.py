import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "UP"

def test_ingest_and_query():
    # 1. Test Ingestion
    doc = "Terraform is an open-source infrastructure as code software tool created by HashiCorp."
    ingest_res = client.post("/ingest", json={"document_text": doc})
    assert ingest_res.status_code == 200
    assert ingest_res.json()["status"] == "success"

    # 2. Test RAG Query
    query_res = client.post("/query", json={"question": "What is Terraform?", "top_k": 1})
    assert query_res.status_code == 200
    data = query_res.json()
    assert data["question"] == "What is Terraform?"
    assert len(data["retrieved_contexts"]) > 0
    assert "HashiCorp" in data["retrieved_contexts"][0]
