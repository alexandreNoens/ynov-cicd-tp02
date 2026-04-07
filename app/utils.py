import re
import unicodedata
from datetime import date


def capitalize(text: str | None) -> str:
    if not text:
        return ""

    return text[:1].upper() + text[1:].lower()


def calculate_average(numbers: list[float] | None) -> float:
    if not numbers:
        return 0

    return round(sum(numbers) / len(numbers), 2)


def slugify(text: str | None) -> str:
    if not text:
        return ""

    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    lowered = ascii_text.lower().strip()
    cleaned = re.sub(r"[^a-z0-9\s-]", "", lowered)
    return re.sub(r"\s+", "-", cleaned).strip("-")


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(value, maximum))


def sort_students(
    students: list[dict[str, str | int | float]] | None,
    sort_by: str,
    order: str = "asc",
) -> list[dict[str, str | int | float]]:
    if not students:
        return []

    return sorted(
        students,
        key=lambda student: student[sort_by],
        reverse=order == "desc",
    )


def calculate_delivery_fee(distance: float, weight: float) -> float | None:
    if distance < 0:
        raise ValueError("Distance cannot be negative.")
    if weight < 0:
        raise ValueError("Weight cannot be negative.")
    if distance > 10:
        return None

    fee = 2.0
    if distance > 3:
        fee += (distance - 3) * 0.5
    if weight > 5:
        fee += 1.5

    return round(fee, 2)


def apply_promo_code(
    subtotal: float,
    promo_code: str | None,
    promo_codes: list[dict[str, str | int | float]] | None,
) -> float:
    if subtotal < 0:
        raise ValueError("Subtotal cannot be negative.")
    if not promo_code:
        return round(subtotal, 2)

    available_codes = promo_codes or []
    promo = next(
        (code for code in available_codes if code.get("code") == promo_code),
        None,
    )
    if promo is None:
        raise ValueError("Promo code does not exist.")

    expires_at = date.fromisoformat(str(promo["expiresAt"]))
    if expires_at < date.today():
        return round(subtotal, 2)

    min_order = float(promo.get("minOrder", 0))
    if subtotal < min_order:
        return round(subtotal, 2)

    promo_type = promo.get("type")
    value = float(promo.get("value", 0))
    if promo_type == "percentage":
        discount = subtotal * (value / 100)
    elif promo_type == "fixed":
        discount = value
    else:
        raise ValueError("Invalid promo code type.")

    return round(max(0.0, subtotal - discount), 2)


def calculate_surge(hour: float, day_of_week: str) -> float:
    day_key = (
        unicodedata.normalize("NFKD", day_of_week)
        .encode("ascii", "ignore")
        .decode("ascii")
        .lower()
    )

    if hour < 10 or hour > 22:
        return 0.0

    if day_key in {"sunday", "dimanche"}:
        return 1.2

    if day_key in {"friday", "vendredi", "saturday", "samedi"}:
        if 19 <= hour <= 22:
            return 1.8
        return 1.0

    if day_key in {
        "monday",
        "lundi",
        "tuesday",
        "mardi",
        "wednesday",
        "mercredi",
        "thursday",
        "jeudi",
    }:
        if 12 <= hour <= 13.5:
            return 1.3
        if 19 <= hour <= 21:
            return 1.5
        if (10 <= hour <= 11.5) or (14 <= hour <= 18):
            return 1.0
        return 1.0

    return 1.0


DEFAULT_PROMO_CODES: list[dict[str, str | int | float]] = [
    {
        "code": "BIENVENUE20",
        "type": "percentage",
        "value": 20,
        "minOrder": 15.0,
        "expiresAt": "2099-12-31",
    },
    {
        "code": "SAVE5",
        "type": "fixed",
        "value": 5,
        "minOrder": 20.0,
        "expiresAt": "2099-12-31",
    },
]


def calculate_order_total(
    items: list[dict[str, str | int | float]],
    distance: float,
    weight: float,
    promo_code: str | None,
    hour: float,
    day_of_week: str,
    promo_codes: list[dict[str, str | int | float]] | None = None,
) -> dict[str, float]:
    if not items:
        raise ValueError("Items cannot be empty.")

    subtotal = 0.0
    for item in items:
        price = float(item.get("price", 0))
        quantity = int(item.get("quantity", 0))

        if price < 0:
            raise ValueError("Item price cannot be negative.")
        if quantity < 0:
            raise ValueError("Item quantity cannot be negative.")
        if quantity == 0:
            continue

        subtotal += price * quantity

    subtotal = round(subtotal, 2)
    discounted_subtotal = apply_promo_code(
        subtotal,
        promo_code,
        promo_codes if promo_codes is not None else DEFAULT_PROMO_CODES,
    )
    discount = round(subtotal - discounted_subtotal, 2)

    delivery_fee = calculate_delivery_fee(distance, weight)
    if delivery_fee is None:
        raise ValueError("Delivery distance is out of service area.")

    surge = calculate_surge(hour, day_of_week)
    if surge == 0:
        raise ValueError("Store is closed at this time.")

    total = round(discounted_subtotal + (delivery_fee * surge), 2)

    return {
        "subtotal": subtotal,
        "discount": discount,
        "deliveryFee": round(delivery_fee, 2),
        "surge": surge,
        "total": total,
    }
