import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routes.orders import orders_store


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(autouse=True)
def clear_orders_store() -> None:
    """Clear orders store before each test to avoid state leakage."""
    orders_store.clear()
    yield
    orders_store.clear()
