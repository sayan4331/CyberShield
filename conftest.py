"""
Shared pytest fixtures. Points the app at a throwaway SQLite file for the
duration of the test session so tests never touch the real dev database.
"""
import os
import tempfile
from pathlib import Path

import pytest

_tmp_dir = tempfile.mkdtemp(prefix="cybershield_test_")
os.environ["CYBERSHIELD_DATABASE_URL"] = f"sqlite:///{Path(_tmp_dir) / 'test.db'}"
os.environ["CYBERSHIELD_DEBUG"] = "true"

from fastapi.testclient import TestClient  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c
