import os
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def auth_header():
    token = os.getenv("API_TOKEN")
    return {"Authorization": f"Bearer {token}"}
