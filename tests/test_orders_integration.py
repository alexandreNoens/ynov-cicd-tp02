from fastapi.testclient import TestClient

from app.routes.orders import orders_store

# ============================================================================
# POST /orders/simulate - 7+ tests
# ============================================================================


def test_should_simulate_order_and_return_correct_price(
	client: TestClient,
) -> None:
	# Arrange
	payload = {
		"items": [{"name": "Pizza", "price": 12.50, "quantity": 2}],
		"distance": 5.0,
		"weight": 2.0,
		"promo_code": None,
		"hour": 15.0,
		"day_of_week": "mardi",
	}

	# Act
	response = client.post("/orders/simulate", json=payload)

	# Assert
	assert response.status_code == 200
	data = response.json()
	assert data["subtotal"] == 25.0
	assert data["deliveryFee"] == 3.0
	assert data["surge"] == 1.0
	assert data["total"] == 28.0
	assert len(orders_store) == 0


def test_should_apply_valid_promo_code_in_simulation(
	client: TestClient,
) -> None:
	# Arrange
	payload = {
		"items": [{"name": "Pizza", "price": 12.50, "quantity": 2}],
		"distance": 5.0,
		"weight": 2.0,
		"promo_code": "BIENVENUE20",
		"hour": 15.0,
		"day_of_week": "mardi",
	}

	# Act
	response = client.post("/orders/simulate", json=payload)

	# Assert
	assert response.status_code == 200
	data = response.json()
	assert data["subtotal"] == 25.0
	assert data["discount"] == 5.0
	assert data["total"] == 23.0


def test_should_reject_expired_promo_code_in_simulation(
	client: TestClient,
) -> None:
	# Arrange
	payload = {
		"items": [{"name": "Pizza", "price": 12.50, "quantity": 2}],
		"distance": 5.0,
		"weight": 2.0,
		"promo_code": "EXPIRED2025",
		"hour": 15.0,
		"day_of_week": "mardi",
	}

	# Act
	response = client.post("/orders/simulate", json=payload)

	# Assert
	assert response.status_code == 400
	assert "expired" in response.json()["detail"].lower()


def test_should_reject_empty_items_in_simulation(
	client: TestClient,
) -> None:
	# Arrange
	payload = {
		"items": [],
		"distance": 5.0,
		"weight": 2.0,
		"promo_code": None,
		"hour": 15.0,
		"day_of_week": "mardi",
	}

	# Act
	response = client.post("/orders/simulate", json=payload)

	# Assert
	assert response.status_code == 400
	assert "empty" in response.json()["detail"].lower()


def test_should_reject_out_of_service_area_in_simulation(
	client: TestClient,
) -> None:
	# Arrange
	payload = {
		"items": [{"name": "Pizza", "price": 12.50, "quantity": 1}],
		"distance": 15.0,
		"weight": 2.0,
		"promo_code": None,
		"hour": 15.0,
		"day_of_week": "mardi",
	}

	# Act
	response = client.post("/orders/simulate", json=payload)

	# Assert
	assert response.status_code == 400
	assert "service area" in response.json()["detail"].lower()


def test_should_reject_closed_hours_in_simulation(
	client: TestClient,
) -> None:
	# Arrange
	payload = {
		"items": [{"name": "Pizza", "price": 12.50, "quantity": 1}],
		"distance": 5.0,
		"weight": 2.0,
		"promo_code": None,
		"hour": 23.0,
		"day_of_week": "mardi",
	}

	# Act
	response = client.post("/orders/simulate", json=payload)

	# Assert
	assert response.status_code == 400
	assert "closed" in response.json()["detail"].lower()


def test_should_apply_surge_to_delivery_fee_only(
	client: TestClient,
) -> None:
	# Arrange
	payload = {
		"items": [{"name": "Pizza", "price": 12.50, "quantity": 2}],
		"distance": 5.0,
		"weight": 2.0,
		"promo_code": None,
		"hour": 20.0,
		"day_of_week": "vendredi",
	}

	# Act
	response = client.post("/orders/simulate", json=payload)

	# Assert
	assert response.status_code == 200
	data = response.json()
	assert data["subtotal"] == 25.0
	assert data["deliveryFee"] == 3.0
	assert data["surge"] == 1.8
	assert data["total"] == 30.4


# ============================================================================
# POST /orders - 5+ tests
# ============================================================================


def test_should_create_order_with_201_status_and_id(
	client: TestClient,
) -> None:
	# Arrange
	payload = {
		"items": [{"name": "Pizza", "price": 12.50, "quantity": 2}],
		"distance": 5.0,
		"weight": 2.0,
		"promo_code": None,
		"hour": 15.0,
		"day_of_week": "mardi",
	}

	# Act
	response = client.post("/orders", json=payload)

	# Assert
	assert response.status_code == 201
	data = response.json()
	assert "id" in data
	assert data["subtotal"] == 25.0
	assert data["total"] == 28.0


def test_should_create_order_and_be_retrievable_by_id(
	client: TestClient,
) -> None:
	# Arrange
	payload = {
		"items": [{"name": "Pizza", "price": 12.50, "quantity": 1}],
		"distance": 5.0,
		"weight": 2.0,
		"promo_code": None,
		"hour": 15.0,
		"day_of_week": "mardi",
	}

	# Act - Create order
	create_response = client.post("/orders", json=payload)
	order_id = create_response.json()["id"]

	# Act - Get order
	get_response = client.get(f"/orders/{order_id}")

	# Assert
	assert get_response.status_code == 200
	data = get_response.json()
	assert data["id"] == order_id
	assert data["subtotal"] == 12.50
	assert data["total"] == 15.50


def test_should_create_multiple_orders_with_different_ids(
	client: TestClient,
) -> None:
	# Arrange
	payload1 = {
		"items": [{"name": "Pizza", "price": 10.0, "quantity": 1}],
		"distance": 3.0,
		"weight": 1.0,
		"promo_code": None,
		"hour": 15.0,
		"day_of_week": "mardi",
	}
	payload2 = {
		"items": [{"name": "Burger", "price": 15.0, "quantity": 1}],
		"distance": 4.0,
		"weight": 1.5,
		"promo_code": None,
		"hour": 15.0,
		"day_of_week": "mardi",
	}

	# Act
	response1 = client.post("/orders", json=payload1)
	response2 = client.post("/orders", json=payload2)

	# Assert
	assert response1.status_code == 201
	assert response2.status_code == 201
	id1 = response1.json()["id"]
	id2 = response2.json()["id"]
	assert id1 != id2
	assert len(orders_store) == 2


def test_should_reject_invalid_order_with_400(
	client: TestClient,
) -> None:
	# Arrange
	payload = {
		"items": [],
		"distance": 5.0,
		"weight": 2.0,
		"promo_code": None,
		"hour": 15.0,
		"day_of_week": "mardi",
	}

	# Act
	response = client.post("/orders", json=payload)

	# Assert
	assert response.status_code == 400
	assert len(orders_store) == 0


def test_should_not_save_invalid_order(
	client: TestClient,
) -> None:
	# Arrange
	invalid_payload = {
		"items": [],
		"distance": 5.0,
		"weight": 2.0,
		"promo_code": None,
		"hour": 15.0,
		"day_of_week": "mardi",
	}
	valid_payload = {
		"items": [{"name": "Pizza", "price": 12.50, "quantity": 1}],
		"distance": 5.0,
		"weight": 2.0,
		"promo_code": None,
		"hour": 15.0,
		"day_of_week": "mardi",
	}

	# Act
	response_invalid = client.post("/orders", json=invalid_payload)
	response_valid = client.post("/orders", json=valid_payload)

	# Assert
	assert response_invalid.status_code == 400
	assert response_valid.status_code == 201
	assert len(orders_store) == 1


# ============================================================================
# GET /orders/:id - 3+ tests
# ============================================================================


def test_should_retrieve_existing_order_with_correct_structure(
	client: TestClient,
) -> None:
	# Arrange
	payload = {
		"items": [{"name": "Pizza", "price": 12.50, "quantity": 2}],
		"distance": 5.0,
		"weight": 2.0,
		"promo_code": "BIENVENUE20",
		"hour": 15.0,
		"day_of_week": "mardi",
	}

	# Act - Create order
	create_response = client.post("/orders", json=payload)
	order_id = create_response.json()["id"]

	# Act - Get order
	get_response = client.get(f"/orders/{order_id}")

	# Assert
	assert get_response.status_code == 200
	data = get_response.json()
	assert data["id"] == order_id
	assert isinstance(data["items"], list)
	assert data["distance"] == 5.0
	assert data["weight"] == 2.0
	assert data["promoCode"] == "BIENVENUE20"
	assert data["hour"] == 15.0
	assert data["dayOfWeek"] == "mardi"
	assert "subtotal" in data
	assert "deliveryFee" in data
	assert "surge" in data
	assert "total" in data
	assert "discount" in data


def test_should_return_404_for_nonexistent_order_id(
	client: TestClient,
) -> None:
	# Act
	response = client.get("/orders/nonexistent-id-12345")

	# Assert
	assert response.status_code == 404
	assert "not found" in response.json()["detail"].lower()


def test_should_return_different_orders_without_cross_contamination(
	client: TestClient,
) -> None:
	# Arrange
	payload1 = {
		"items": [{"name": "Pizza", "price": 10.0, "quantity": 1}],
		"distance": 3.0,
		"weight": 1.0,
		"promo_code": None,
		"hour": 15.0,
		"day_of_week": "mardi",
	}
	payload2 = {
		"items": [{"name": "Burger", "price": 20.0, "quantity": 2}],
		"distance": 4.0,
		"weight": 2.0,
		"promo_code": "BIENVENUE20",
		"hour": 18.0,
		"day_of_week": "jeudi",
	}

	# Act
	create1 = client.post("/orders", json=payload1)
	create2 = client.post("/orders", json=payload2)
	get1 = client.get(f"/orders/{create1.json()['id']}")
	get2 = client.get(f"/orders/{create2.json()['id']}")

	# Assert
	assert get1.json()["subtotal"] == 10.0
	assert get2.json()["subtotal"] == 40.0
	assert get1.json()["promoCode"] is None
	assert get2.json()["promoCode"] == "BIENVENUE20"
