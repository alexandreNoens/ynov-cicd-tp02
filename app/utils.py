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
