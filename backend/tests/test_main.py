"""
Test suite for main API endpoints
Ensures 90% coverage requirement
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root health check endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "AI Storytelling Engine API is running"}

def test_health_check():
    """Test the detailed health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "0.1.0"
    assert "milestone" in data

def test_generate_story_success():
    """Test successful story generation with valid input"""
    story_request = {
        "premise": "A cyberpunk detective story",
        "mood": "gritty",
        "characters": "3 characters"
    }
    response = client.post("/api/stories/generate", json=story_request)
    assert response.status_code == 200
    
    data = response.json()
    assert "id" in data
    assert "title" in data
    assert "chapters" in data
    assert len(data["chapters"]) > 0
    assert "Generated Story: A cyberpunk detective story" in data["title"]

def test_generate_story_empty_premise():
    """Test story generation with empty premise"""
    story_request = {"premise": ""}
    response = client.post("/api/stories/generate", json=story_request)
    assert response.status_code == 400
    assert "Story premise is required" in response.json()["detail"]

def test_generate_story_whitespace_premise():
    """Test story generation with whitespace-only premise"""
    story_request = {"premise": "   "}
    response = client.post("/api/stories/generate", json=story_request)
    assert response.status_code == 400
    assert "Story premise is required" in response.json()["detail"]

def test_generate_story_minimal_input():
    """Test story generation with minimal valid input"""
    story_request = {"premise": "Space adventure"}
    response = client.post("/api/stories/generate", json=story_request)
    assert response.status_code == 200
    
    data = response.json()
    assert data["chapters"][0]["choices"]
    assert len(data["chapters"][0]["choices"]) == 3

def test_get_story_endpoint():
    """Test story retrieval endpoint (stub)"""
    response = client.get("/api/stories/test_id")
    assert response.status_code == 200
    assert "test_id" in response.json()["message"]

def test_save_story_endpoint():
    """Test story saving endpoint (stub)"""
    response = client.post("/api/stories/test_id/save")
    assert response.status_code == 200
    assert "test_id" in response.json()["message"]