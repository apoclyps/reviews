import sqlite3

import pytest


@pytest.fixture
def setup_database():
    """Fixture to set up the in-memory database with test data"""
    yield sqlite3.connect(":memory:")
