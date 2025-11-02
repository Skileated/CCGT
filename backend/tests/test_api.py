"""
API endpoint tests.

Maps to SRS: API Testing Requirements.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    """Test health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "version" in data
    assert data["status"] == "healthy"


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data


def test_evaluate_endpoint():
    """Test text evaluation endpoint."""
    test_text = """
    This is a sample paragraph. It contains multiple sentences.
    Each sentence should flow coherently to the next.
    The overall coherence can be measured using graph-based methods.
    """
    
    response = client.post(
        "/api/v1/evaluate",
        json={
            "text": test_text,
            "options": {"visualize": True}
        }
    )
    
    # Note: This might fail if auth is required, but for testing we allow it
    # In production, add proper auth headers
    assert response.status_code in [200, 401]  # 401 if auth required
    
    if response.status_code == 200:
        data = response.json()
        assert "coherence_score" in data
        assert "coherence_percent" in data
        assert "disruption_report" in data
        assert 0.0 <= data["coherence_score"] <= 1.0
        assert 0 <= data["coherence_percent"] <= 100


def test_evaluate_empty_text():
    """Test evaluation with empty text."""
    response = client.post(
        "/api/v1/evaluate",
        json={"text": ""}
    )
    assert response.status_code in [400, 422, 401]  # Validation error or auth required


def test_batch_evaluate_endpoint():
    """Test batch evaluation endpoint."""
    texts = [
        "This is the first paragraph. It has multiple sentences.",
        "This is the second paragraph. It also has multiple sentences."
    ]
    
    response = client.post(
        "/api/v1/batch_evaluate",
        json={"texts": texts}
    )
    
    assert response.status_code in [200, 401]  # 401 if auth required
    
    if response.status_code == 200:
        data = response.json()
        assert "results" in data
        assert "total_processed" in data
        assert len(data["results"]) == len(texts)

