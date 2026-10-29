import pytest
from app.repository.rooms import _ROOMS
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(autouse=True)
def clear_rooms():
    _ROOMS.clear()
    yield
    _ROOMS.clear()
