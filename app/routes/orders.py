import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.utils import calculate_order_total

router = APIRouter(prefix="/orders", tags=["orders"])

orders_store: dict[str, dict[str, Any]] = {}


class OrderItem(BaseModel):
    name: str
    price: float
    quantity: int


class SimulateOrderRequest(BaseModel):
    items: list[OrderItem]
    distance: float
    weight: float
    promo_code: str | None = None
    hour: float = 15.0
    day_of_week: str = "mardi"


@router.post("/simulate")
def simulate_order(
    request: SimulateOrderRequest,
) -> dict[str, Any]:
    """Simulate an order without saving it."""
    try:
        items = [item.model_dump() for item in request.items]
        result = calculate_order_total(
            items,
            request.distance,
            request.weight,
            request.promo_code,
            request.hour,
            request.day_of_week,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("")
def create_order(
    request: SimulateOrderRequest,
) -> dict[str, Any]:
    """Create an order and save it in memory."""
    try:
        items = [item.model_dump() for item in request.items]
        order_detail = calculate_order_total(
            items,
            request.distance,
            request.weight,
            request.promo_code,
            request.hour,
            request.day_of_week,
        )
        order_id = str(uuid.uuid4())
        order_data = {
            "id": order_id,
            "items": items,
            "distance": request.distance,
            "weight": request.weight,
            "promoCode": request.promo_code,
            "hour": request.hour,
            "dayOfWeek": request.day_of_week,
            **order_detail,
        }
        orders_store[order_id] = order_data
        return order_data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{order_id}")
def get_order(order_id: str) -> dict[str, Any]:
    """Retrieve an order by ID."""
    if order_id not in orders_store:
        raise HTTPException(status_code=404, detail="Order not found.")
    return orders_store[order_id]
