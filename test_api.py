import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Social Media Video Downloader API"}

def test_get_supported_platforms():
    response = client.get("/api/v1/supported-platforms")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_download_video_unauthorized():
    # Test without authentication
    response = client.post(
        "/api/v1/download",
        json={
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "platform": "youtube",
            "quality": "720p"
        }
    )
    assert response.status_code == 401  # Unauthorized

def test_login():
    # Test login with test user
    response = client.post(
        "/auth/login",
        data={
            "username": "testuser",
            "password": "secret"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
