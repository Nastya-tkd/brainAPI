from fastapi.testclient import TestClient
from .main import app
from .database import SessionLocal, engine
from . import models

client = TestClient(app)

def setup_module():
    models.Base.metadata.create_all(bind=engine)

def teardown_module():
    models.Base.metadata.drop_all(bind=engine)

def test_create_nanoparticle():
    response = client.post(
        "/nanoparticles/",
        json={
            "nanoparticle_type": "Test NP",
            "experiment_condition": "Test Condition",
            "mouse_number": 1,
            "lungs": 10.0,
            "liver": 20.0,
            "kidneys": 5.0,
            "spleen": 2.0,
            "brain": 1.0,
            "heart": 0.5
        },
        headers={"Authorization": "Bearer testtoken"}
    )
    assert response.status_code == 200
    assert response.json()["nanoparticle_type"] == "Test NP"

def test_get_nanoparticles():
    response = client.get("/nanoparticles/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_compare_nanoparticles():
    response = client.get("/analysis/compare?organ=liver&nanoparticle_types=Test NP")
    assert response.status_code == 200
    assert len(response.json()) > 0