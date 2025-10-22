"""
Basic tests for Document Ingestion Service
"""
import sys
import os
import pytest
from pathlib import Path

# Add the parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "Document Ingestion Service"
    assert data["version"] == "1.0.0"

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health/")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "timestamp" in data

def test_upload_without_api_key():
    """Test upload endpoint without API key"""
    response = client.post("/documents/upload")
    assert response.status_code == 422  # Validation error

def test_upload_with_invalid_api_key():
    """Test upload endpoint with invalid API key"""
    response = client.post(
        "/documents/upload",
        params={"api_key": "invalid-key"}
    )
    assert response.status_code == 401

def test_list_documents_without_api_key():
    """Test list documents without API key"""
    response = client.get("/documents/")
    assert response.status_code == 422  # Validation error
