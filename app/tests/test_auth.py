from fastapi.testclient import TestClient
from .main import app
from .database import SessionLocal, engine
from . import models

client = TestClient(app)

def test_register():
    response = client.post(
        "/register",
        json={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_login():
    response = client.post(
        "/login",
        json={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()