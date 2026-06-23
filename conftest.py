"""Pytest setup: point the database at a throwaway temp file BEFORE src.db loads,
and seed it fresh for each test. Keeps tests from touching the real maintenance.db.
"""
import os
import tempfile

# Must run before `from src import db` anywhere — db reads this env var at import.
os.environ["MAINTENANCE_DB"] = os.path.join(tempfile.gettempdir(), "test_maintenance.db")
try:
    os.remove(os.environ["MAINTENANCE_DB"])
except OSError:
    pass

import pytest  # noqa: E402

from src import db  # noqa: E402


@pytest.fixture(autouse=True)
def _seed_db():
    db.init_db()
    yield
