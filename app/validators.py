import re

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
SPECIAL_PATTERN = re.compile(r"[!@#$%^&*]")


def is_valid_email(email: str | None) -> bool:
    if not email:
        return False

    return bool(EMAIL_PATTERN.match(email))


def is_valid_password(password: str | None) -> dict[str, bool | list[str]]:
    pwd = password or ""
    errors: list[str] = []

    if len(pwd) < 8:
        errors.append("Password must be at least 8 characters long.")
    if not any(char.isupper() for char in pwd):
        errors.append("Password must contain at least one uppercase letter.")
    if not any(char.islower() for char in pwd):
        errors.append("Password must contain at least one lowercase letter.")
    if not any(char.isdigit() for char in pwd):
        errors.append("Password must contain at least one digit.")
    if not SPECIAL_PATTERN.search(pwd):
        errors.append(
            "Password must contain at least one special character (!@#$%^&*)."
        )

    return {"valid": len(errors) == 0, "errors": errors}


def is_valid_age(age: int | None) -> bool:
    if isinstance(age, bool) or not isinstance(age, int):
        return False

    return 0 <= age <= 150
