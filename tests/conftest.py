import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module

# keep a pristine copy of the initial activities so tests can reset state
_original_activities = copy.deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    """Restore the in-memory activities dict before each test."""
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(_original_activities))
    yield
    # nothing special after


@pytest.fixture

def client():
    """Return a TestClient instance configured for the FastAPI app."""
    return TestClient(app_module.app)
