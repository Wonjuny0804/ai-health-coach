import pytest
from fastapi.testclient import TestClient

from tests.test_app import app

@pytest.fixture
def test_client():
    """Create a test client for FastAPI"""
    with TestClient(app) as client:
        yield client
