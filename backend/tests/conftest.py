import pytest
from app.repository.rooms import _ROOMS


@pytest.fixture(autouse=True)
def clear_rooms():
    _ROOMS.clear()
    yield
    _ROOMS.clear()
