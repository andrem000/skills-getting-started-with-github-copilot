from fastapi.testclient import TestClient
import importlib
import pytest


@pytest.fixture

def client():
    # Import and reload to reset module-level state between tests
    app_module = importlib.import_module("src.app")
    importlib.reload(app_module)
    return TestClient(app_module.app)
