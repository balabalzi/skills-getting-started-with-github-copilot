import copy
import pytest
from fastapi.testclient import TestClient

from src.app import app, activities as _activities


@pytest.fixture(scope="function")
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def restore_activities():
    """Deep-copy the initial activities and restore after each test to keep tests isolated."""
    original = copy.deepcopy(_activities)
    yield
    # Clear and restore
    _activities.clear()
    _activities.update(original)
