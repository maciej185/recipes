"""General fixtures for the test suite."""

import pytest

from src.dependencies import get_db
from src.main import app

from .db import override_get_db


@pytest.fixture(autouse=True)
def override_get_db_for_each_test():
    """Override the 'get_db' dependency and return to original dependency after each test."""
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides = {}
