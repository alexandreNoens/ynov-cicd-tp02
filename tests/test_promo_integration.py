from fastapi.testclient import TestClient

# ============================================================================
# POST /promo/validate - 5+ tests
# ============================================================================


def test_should_validate_valid_promo_code_and_return_discount(
	client: TestClient,
) -> None:
	# Arrange
	payload = {
		"promo_code": "BIENVENUE20",
		"subtotal": 25.0,
	}

	# Act
	response = client.post("/promo/validate", json=payload)

	# Assert
	assert response.status_code == 200
	data = response.json()
	assert data["valid"] is True
	assert data["originalPrice"] == 25.0
	assert data["newPrice"] == 20.0
	assert data["discount"] == 5.0


def test_should_reject_expired_promo_code_with_400(
	client: TestClient,
) -> None:
	# Arrange
	payload = {
		"promo_code": "EXPIRED2025",
		"subtotal": 25.0,
	}

	# Act
	response = client.post("/promo/validate", json=payload)

	# Assert
	assert response.status_code == 400
	assert "expired" in response.json()["detail"].lower()


def test_should_reject_subtotal_below_minimum_with_400(
	client: TestClient,
) -> None:
	# Arrange
	payload = {
		"promo_code": "SAVE5",
		"subtotal": 15.0,
	}

	# Act
	response = client.post("/promo/validate", json=payload)

	# Assert
	assert response.status_code == 400
	assert "minimum" in response.json()["detail"].lower()


def test_should_reject_unknown_promo_code_with_404(
	client: TestClient,
) -> None:
	# Arrange
	payload = {
		"promo_code": "NONEXISTENT",
		"subtotal": 25.0,
	}

	# Act
	response = client.post("/promo/validate", json=payload)

	# Assert
	assert response.status_code == 404
	assert "does not exist" in response.json()["detail"].lower()


def test_should_return_400_when_required_field_missing(
	client: TestClient,
) -> None:
	# Arrange
	payload = {
		"subtotal": 25.0,
	}

	# Act
	response = client.post("/promo/validate", json=payload)

	# Assert
	assert response.status_code == 422


def test_should_validate_fixed_discount_promo_code(
	client: TestClient,
) -> None:
	# Arrange
	payload = {
		"promo_code": "SAVE5",
		"subtotal": 25.0,
	}

	# Act
	response = client.post("/promo/validate", json=payload)

	# Assert
	assert response.status_code == 200
	data = response.json()
	assert data["valid"] is True
	assert data["originalPrice"] == 25.0
	assert data["newPrice"] == 20.0
	assert data["discount"] == 5.0


def test_should_validate_promo_on_different_subtotals(
	client: TestClient,
) -> None:
	# Arrange
	payload = {
		"promo_code": "BIENVENUE20",
		"subtotal": 50.0,
	}

	# Act
	response = client.post("/promo/validate", json=payload)

	# Assert
	assert response.status_code == 200
	data = response.json()
	assert data["valid"] is True
	assert data["originalPrice"] == 50.0
	assert data["newPrice"] == 40.0
	assert data["discount"] == 10.0
