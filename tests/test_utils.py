from app.utils import (
    calculate_average,
    capitalize,
    clamp,
    slugify,
    sort_students,
)


def test_should_capitalize_first_letter_when_text_is_lowercase() -> None:
    # Arrange
    value = "hello"

    # Act
    result = capitalize(value)

    # Assert
    assert result == "Hello"


def test_should_normalize_case_when_text_is_uppercase() -> None:
    # Arrange
    value = "WORLD"

    # Act
    result = capitalize(value)

    # Assert
    assert result == "World"


def test_should_return_empty_string_when_text_is_empty() -> None:
    # Arrange
    value = ""

    # Act
    result = capitalize(value)

    # Assert
    assert result == ""


def test_should_return_empty_string_when_text_is_none() -> None:
    # Arrange
    value = None

    # Act
    result = capitalize(value)

    # Assert
    assert result == ""


def test_should_return_average_when_list_contains_multiple_numbers() -> None:
    # Arrange
    values = [10, 12, 14]

    # Act
    result = calculate_average(values)

    # Assert
    assert result == 12


def test_should_return_same_value_when_list_contains_single_number() -> None:
    # Arrange
    values = [15]

    # Act
    result = calculate_average(values)

    # Assert
    assert result == 15


def test_should_return_zero_when_list_is_empty() -> None:
    # Arrange
    values: list[int] = []

    # Act
    result = calculate_average(values)

    # Assert
    assert result == 0


def test_should_return_zero_when_list_is_none() -> None:
    # Arrange
    values = None

    # Act
    result = calculate_average(values)

    # Assert
    assert result == 0


def test_should_round_average_to_two_decimals_when_needed() -> None:
    # Arrange
    values = [10, 10, 11]

    # Act
    result = calculate_average(values)

    # Assert
    assert result == 10.33


def test_should_convert_text_to_slug_when_text_has_spaces() -> None:
    # Arrange
    value = "Hello World"

    # Act
    result = slugify(value)

    # Assert
    assert result == "hello-world"


def test_should_trim_and_collapse_spaces_when_text_has_extra_spaces() -> None:
    # Arrange
    value = " Spaces Everywhere "

    # Act
    result = slugify(value)

    # Assert
    assert result == "spaces-everywhere"


def test_should_remove_special_characters_when_text_contains_punctuation() -> (
    None
):
    # Arrange
    value = "C'est l'ete !"

    # Act
    result = slugify(value)

    # Assert
    assert result == "cest-lete"


def test_should_return_empty_slug_when_text_is_empty() -> None:
    # Arrange
    value = ""

    # Act
    result = slugify(value)

    # Assert
    assert result == ""


def test_should_keep_value_when_value_is_within_range() -> None:
    # Arrange
    value, minimum, maximum = 5, 0, 10

    # Act
    result = clamp(value, minimum, maximum)

    # Assert
    assert result == 5


def test_should_return_minimum_when_value_is_below_range() -> None:
    # Arrange
    value, minimum, maximum = -5, 0, 10

    # Act
    result = clamp(value, minimum, maximum)

    # Assert
    assert result == 0


def test_should_return_maximum_when_value_is_above_range() -> None:
    # Arrange
    value, minimum, maximum = 15, 0, 10

    # Act
    result = clamp(value, minimum, maximum)

    # Assert
    assert result == 10


def test_should_return_value_when_minimum_equals_maximum() -> None:
    # Arrange
    value, minimum, maximum = 0, 0, 0

    # Act
    result = clamp(value, minimum, maximum)

    # Assert
    assert result == 0


def test_should_sort_students_by_grade_ascending() -> None:
    # Arrange
    students = [
        {"name": "Zoe", "grade": 14, "age": 20},
        {"name": "Alice", "grade": 10, "age": 22},
        {"name": "Bob", "grade": 12, "age": 19},
    ]

    # Act
    result = sort_students(students, "grade", "asc")

    # Assert
    assert [student["grade"] for student in result] == [10, 12, 14]


def test_should_sort_students_by_grade_descending() -> None:
    # Arrange
    students = [
        {"name": "Zoe", "grade": 14, "age": 20},
        {"name": "Alice", "grade": 10, "age": 22},
        {"name": "Bob", "grade": 12, "age": 19},
    ]

    # Act
    result = sort_students(students, "grade", "desc")

    # Assert
    assert [student["grade"] for student in result] == [14, 12, 10]


def test_should_sort_students_by_name_ascending() -> None:
    # Arrange
    students = [
        {"name": "Zoe", "grade": 14, "age": 20},
        {"name": "Alice", "grade": 10, "age": 22},
        {"name": "Bob", "grade": 12, "age": 19},
    ]

    # Act
    result = sort_students(students, "name", "asc")

    # Assert
    assert [student["name"] for student in result] == ["Alice", "Bob", "Zoe"]


def test_should_sort_students_by_age_ascending() -> None:
    # Arrange
    students = [
        {"name": "Zoe", "grade": 14, "age": 20},
        {"name": "Alice", "grade": 10, "age": 22},
        {"name": "Bob", "grade": 12, "age": 19},
    ]

    # Act
    result = sort_students(students, "age", "asc")

    # Assert
    assert [student["age"] for student in result] == [19, 20, 22]


def test_should_return_empty_array_for_null_input() -> None:
    # Arrange
    students = None

    # Act
    result = sort_students(students, "grade", "asc")

    # Assert
    assert result == []


def test_should_return_empty_array_for_empty_input() -> None:
    # Arrange
    students: list[dict[str, str | int | float]] = []

    # Act
    result = sort_students(students, "grade", "asc")

    # Assert
    assert result == []


def test_should_not_modify_the_original_array() -> None:
    # Arrange
    students = [
        {"name": "Zoe", "grade": 14, "age": 20},
        {"name": "Alice", "grade": 10, "age": 22},
        {"name": "Bob", "grade": 12, "age": 19},
    ]
    original = [student.copy() for student in students]

    # Act
    result = sort_students(students, "grade", "asc")

    # Assert
    assert students == original
    assert result is not students


def test_should_default_to_ascending_order() -> None:
    # Arrange
    students = [
        {"name": "Zoe", "grade": 14, "age": 20},
        {"name": "Alice", "grade": 10, "age": 22},
        {"name": "Bob", "grade": 12, "age": 19},
    ]

    # Act
    result = sort_students(students, "grade")

    # Assert
    assert [student["grade"] for student in result] == [10, 12, 14]
