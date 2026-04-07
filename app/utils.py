import re
import unicodedata


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
