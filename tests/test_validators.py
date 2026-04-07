from app.validators import is_valid_age, is_valid_email, is_valid_password


def test_should_return_true_when_email_is_standard_valid() -> None:
    # Arrange
    email = "user@example.com"

    # Act
    result = is_valid_email(email)

    # Assert
    assert result is True


def test_should_return_true_when_email_has_plus_tag_and_subdomain() -> None:
    # Arrange
    email = "user.name+tag@domain.co"

    # Act
    result = is_valid_email(email)

    # Assert
    assert result is True


def test_should_return_false_when_email_has_no_at_symbol() -> None:
    # Arrange
    email = "invalid"

    # Act
    result = is_valid_email(email)

    # Assert
    assert result is False


def test_should_return_false_when_email_has_no_local_part() -> None:
    # Arrange
    email = "@domain.com"

    # Act
    result = is_valid_email(email)

    # Assert
    assert result is False


def test_should_return_false_when_email_has_no_domain_part() -> None:
    # Arrange
    email = "user@"

    # Act
    result = is_valid_email(email)

    # Assert
    assert result is False


def test_should_return_false_when_email_is_empty() -> None:
    # Arrange
    email = ""

    # Act
    result = is_valid_email(email)

    # Assert
    assert result is False


def test_should_return_false_when_email_is_none() -> None:
    # Arrange
    email = None

    # Act
    result = is_valid_email(email)

    # Assert
    assert result is False


def test_should_return_valid_true_when_password_matches_all_rules() -> None:
    # Arrange
    password = "Passw0rd!"

    # Act
    result = is_valid_password(password)

    # Assert
    assert result == {"valid": True, "errors": []}


def test_should_return_expected_errors_when_password_is_short() -> None:
    # Arrange
    password = "short"

    # Act
    result = is_valid_password(password)

    # Assert
    assert result["valid"] is False
    assert result["errors"] == [
        "Password must be at least 8 characters long.",
        "Password must contain at least one uppercase letter.",
        "Password must contain at least one digit.",
        "Password must contain at least one special character (!@#$%^&*).",
    ]


def test_should_return_uppercase_error_when_password_has_no_uppercase() -> None:
    # Arrange
    password = "alllowercase1!"

    # Act
    result = is_valid_password(password)

    # Assert
    assert result["valid"] is False
    assert result["errors"] == [
        "Password must contain at least one uppercase letter."
    ]


def test_should_return_lowercase_error_when_password_has_no_lowercase() -> None:
    # Arrange
    password = "ALLUPPERCASE1!"

    # Act
    result = is_valid_password(password)

    # Assert
    assert result["valid"] is False
    assert result["errors"] == [
        "Password must contain at least one lowercase letter."
    ]


def test_should_return_digit_error_when_password_has_no_digit() -> None:
    # Arrange
    password = "NoDigits!here"

    # Act
    result = is_valid_password(password)

    # Assert
    assert result["valid"] is False
    assert result["errors"] == ["Password must contain at least one digit."]


def test_should_return_special_char_error_when_password_has_no_special() -> (
    None
):
    # Arrange
    password = "NoSpecial1here"

    # Act
    result = is_valid_password(password)

    # Assert
    assert result["valid"] is False
    assert result["errors"] == [
        "Password must contain at least one special character (!@#$%^&*)."
    ]


def test_should_return_all_errors_when_password_is_empty() -> None:
    # Arrange
    password = ""

    # Act
    result = is_valid_password(password)

    # Assert
    assert result["valid"] is False
    assert result["errors"] == [
        "Password must be at least 8 characters long.",
        "Password must contain at least one uppercase letter.",
        "Password must contain at least one lowercase letter.",
        "Password must contain at least one digit.",
        "Password must contain at least one special character (!@#$%^&*).",
    ]


def test_should_return_all_errors_when_password_is_none() -> None:
    # Arrange
    password = None

    # Act
    result = is_valid_password(password)

    # Assert
    assert result["valid"] is False
    assert result["errors"] == [
        "Password must be at least 8 characters long.",
        "Password must contain at least one uppercase letter.",
        "Password must contain at least one lowercase letter.",
        "Password must contain at least one digit.",
        "Password must contain at least one special character (!@#$%^&*).",
    ]


def test_should_return_true_when_age_is_valid_integer() -> None:
    # Arrange
    age = 25

    # Act
    result = is_valid_age(age)

    # Assert
    assert result is True


def test_should_return_true_when_age_is_lower_bound() -> None:
    # Arrange
    age = 0

    # Act
    result = is_valid_age(age)

    # Assert
    assert result is True


def test_should_return_true_when_age_is_upper_bound() -> None:
    # Arrange
    age = 150

    # Act
    result = is_valid_age(age)

    # Assert
    assert result is True


def test_should_return_false_when_age_is_negative() -> None:
    # Arrange
    age = -1

    # Act
    result = is_valid_age(age)

    # Assert
    assert result is False


def test_should_return_false_when_age_is_greater_than_upper_bound() -> None:
    # Arrange
    age = 151

    # Act
    result = is_valid_age(age)

    # Assert
    assert result is False


def test_should_return_false_when_age_is_not_integer() -> None:
    # Arrange
    age = 25.5

    # Act
    result = is_valid_age(age)

    # Assert
    assert result is False


def test_should_return_false_when_age_is_string() -> None:
    # Arrange
    age = "25"

    # Act
    result = is_valid_age(age)

    # Assert
    assert result is False


def test_should_return_false_when_age_is_none() -> None:
    # Arrange
    age = None

    # Act
    result = is_valid_age(age)

    # Assert
    assert result is False
