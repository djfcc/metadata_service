"""Shared Test fixtures for units tests."""

import pytest
from fastapi import testclient
from metadata_service.main import app


@pytest.fixture(autouse=True)
def client():
    """Create a fixture for the FastAPI test client."""
    return testclient.TestClient(app)
