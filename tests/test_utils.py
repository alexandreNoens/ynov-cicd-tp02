import pytest

from app.utils import (
    calculate_average,
    calculate_delivery_fee,
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


def test_should_return_base_fee_when_distance_is_under_included_range() -> None:
    # Arrange
    distance, weight = 2, 1

    # Act
    result = calculate_delivery_fee(distance, weight)

    # Assert
    assert result == 2.0


def test_should_add_distance_fee_when_distance_is_between_3_and_10() -> None:
    # Arrange
    distance, weight = 7, 3

    # Act
    result = calculate_delivery_fee(distance, weight)

    # Assert
    assert result == 4.0


def test_should_add_heavy_weight_supplement_when_weight_is_above_5kg() -> None:
    # Arrange
    distance, weight = 5, 8

    # Act
    result = calculate_delivery_fee(distance, weight)

    # Assert
    assert result == 4.5


def test_should_return_base_fee_when_distance_is_exactly_3km() -> None:
    # Arrange
    distance, weight = 3, 2

    # Act
    result = calculate_delivery_fee(distance, weight)

    # Assert
    assert result == 2.0


def test_should_accept_order_when_distance_is_exactly_10km() -> None:
    # Arrange
    distance, weight = 10, 4

    # Act
    result = calculate_delivery_fee(distance, weight)

    # Assert
    assert result == 5.5


def test_should_not_add_weight_supplement_when_weight_is_exactly_5kg() -> None:
    # Arrange
    distance, weight = 6, 5

    # Act
    result = calculate_delivery_fee(distance, weight)

    # Assert
    assert result == 3.5


def test_should_return_none_when_distance_is_above_10km() -> None:
    # Arrange
    distance, weight = 15, 2

    # Act
    result = calculate_delivery_fee(distance, weight)

    # Assert
    assert result is None


def test_should_raise_error_when_distance_is_negative() -> None:
    # Arrange
    distance, weight = -1, 2

    # Act / Assert
    with pytest.raises(ValueError, match="Distance cannot be negative"):
        calculate_delivery_fee(distance, weight)


def test_should_raise_error_when_weight_is_negative() -> None:
    # Arrange
    distance, weight = 2, -1

    # Act / Assert
    with pytest.raises(ValueError, match="Weight cannot be negative"):
        calculate_delivery_fee(distance, weight)


def test_should_accept_zero_distance_and_return_base_fee() -> None:
    # Arrange
    distance, weight = 0, 2

    # Act
    result = calculate_delivery_fee(distance, weight)

    # Assert
    assert result == 2.0


def test_should_compute_precise_fee_for_6km_and_2kg() -> None:
    # Arrange
    distance, weight = 6, 2

    # Act
    result = calculate_delivery_fee(distance, weight)

    # Assert
    assert result == 3.5


def test_should_compute_precise_fee_for_10km_and_6kg() -> None:
    # Arrange
    distance, weight = 10, 6

    # Act
    result = calculate_delivery_fee(distance, weight)

    # Assert
    assert result == 7.0
