from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

HEADERS = {"Authorization": "Bearer mock-secret-token"}

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_get_apolice():
    response = client.get("/apolice/12345", headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["numero"] == "12345"

def test_get_apolice_sem_token():
    response = client.get("/apolice/12345")
    assert response.status_code == 422
