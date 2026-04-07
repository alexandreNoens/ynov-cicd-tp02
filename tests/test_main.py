from fastapi.testclient import TestClient

from app.main import app, health


def test_should_return_ok_dict_when_calling_health_function() -> None:
    # Arrange

    # Act
    result = health()

    # Assert
    assert result == {"status": "ok"}


def test_should_return_200_when_calling_health_endpoint() -> None:
    # Arrange
    client = TestClient(app)

    # Act
    response = client.get("/health")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
