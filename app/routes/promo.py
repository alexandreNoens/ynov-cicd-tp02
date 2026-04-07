from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.utils import DEFAULT_PROMO_CODES, apply_promo_code

router = APIRouter(prefix="/promo", tags=["promo"])


class ValidatePromoRequest(BaseModel):
    promo_code: str
    subtotal: float


@router.post("/validate")
def validate_promo(
    request: ValidatePromoRequest,
) -> dict[str, Any]:
    """Validate a promo code and return the new price after discount."""
    try:
        available_codes = DEFAULT_PROMO_CODES
        discounted_subtotal = apply_promo_code(
            request.subtotal, request.promo_code, available_codes
        )
        discount_applied = request.subtotal > discounted_subtotal
        return {
            "valid": discount_applied,
            "originalPrice": request.subtotal,
            "newPrice": discounted_subtotal,
            "discount": request.subtotal - discounted_subtotal,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
