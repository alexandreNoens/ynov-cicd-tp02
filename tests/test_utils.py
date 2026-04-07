from datetime import date

import pytest

from app.utils import (
    apply_promo_code,
    calculate_average,
    calculate_delivery_fee,
    calculate_order_total,
    calculate_surge,
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


def test_should_apply_percentage_promo_when_code_is_valid() -> None:
    # Arrange
    promo_codes = [
        {
            "code": "BIENVENUE20",
            "type": "percentage",
            "value": 20,
            "minOrder": 15.0,
            "expiresAt": "2099-12-31",
        }
    ]

    # Act
    result = apply_promo_code(50.0, "BIENVENUE20", promo_codes)

    # Assert
    assert result == 40.0


def test_should_apply_fixed_promo_when_code_is_valid() -> None:
    # Arrange
    promo_codes = [
        {
            "code": "SAVE5",
            "type": "fixed",
            "value": 5,
            "minOrder": 10.0,
            "expiresAt": "2099-12-31",
        }
    ]

    # Act
    result = apply_promo_code(30.0, "SAVE5", promo_codes)

    # Assert
    assert result == 25.0


def test_should_apply_discount_when_min_order_is_respected() -> None:
    # Arrange
    promo_codes = [
        {
            "code": "MINOK",
            "type": "fixed",
            "value": 5,
            "minOrder": 25.0,
            "expiresAt": "2099-12-31",
        }
    ]

    # Act
    result = apply_promo_code(25.0, "MINOK", promo_codes)

    # Assert
    assert result == 20.0


def test_should_refuse_promo_when_code_is_expired() -> None:
    # Arrange
    promo_codes = [
        {
            "code": "OLD",
            "type": "percentage",
            "value": 20,
            "minOrder": 0.0,
            "expiresAt": "2000-01-01",
        }
    ]

    # Act / Assert
    with pytest.raises(ValueError, match="Promo code has expired"):
        apply_promo_code(50.0, "OLD", promo_codes)


def test_should_refuse_promo_when_subtotal_is_below_min_order() -> None:
    # Arrange
    promo_codes = [
        {
            "code": "MIN30",
            "type": "percentage",
            "value": 10,
            "minOrder": 30.0,
            "expiresAt": "2099-12-31",
        }
    ]

    # Act / Assert
    with pytest.raises(ValueError, match="Minimum order amount"):
        apply_promo_code(20.0, "MIN30", promo_codes)


def test_should_raise_error_when_promo_code_does_not_exist() -> None:
    # Arrange
    promo_codes = []

    # Act / Assert
    with pytest.raises(ValueError, match="Promo code does not exist"):
        apply_promo_code(20.0, "UNKNOWN", promo_codes)


def test_should_return_zero_with_100_percent_promo() -> None:
    # Arrange
    promo_codes = [
        {
            "code": "FREE100",
            "type": "percentage",
            "value": 100,
            "minOrder": 0.0,
            "expiresAt": "2099-12-31",
        }
    ]

    # Act
    result = apply_promo_code(19.0, "FREE100", promo_codes)

    # Assert
    assert result == 0.0


def test_should_keep_zero_subtotal_even_when_promo_is_valid() -> None:
    # Arrange
    promo_codes = [
        {
            "code": "ZERO",
            "type": "fixed",
            "value": 5,
            "minOrder": 0.0,
            "expiresAt": "2099-12-31",
        }
    ]

    # Act
    result = apply_promo_code(0.0, "ZERO", promo_codes)

    # Assert
    assert result == 0.0


def test_should_accept_promo_when_it_expires_today() -> None:
    # Arrange
    promo_codes = [
        {
            "code": "TODAY",
            "type": "fixed",
            "value": 5,
            "minOrder": 0.0,
            "expiresAt": date.today().isoformat(),
        }
    ]

    # Act
    result = apply_promo_code(20.0, "TODAY", promo_codes)

    # Assert
    assert result == 15.0


def test_should_not_apply_discount_when_promo_code_is_none() -> None:
    # Arrange
    promo_codes = [
        {
            "code": "BIENVENUE20",
            "type": "percentage",
            "value": 20,
            "minOrder": 0.0,
            "expiresAt": "2099-12-31",
        }
    ]

    # Act
    result = apply_promo_code(30.0, None, promo_codes)

    # Assert
    assert result == 30.0


def test_should_not_apply_discount_when_promo_code_is_empty() -> None:
    # Arrange
    promo_codes = [
        {
            "code": "BIENVENUE20",
            "type": "percentage",
            "value": 20,
            "minOrder": 0.0,
            "expiresAt": "2099-12-31",
        }
    ]

    # Act
    result = apply_promo_code(30.0, "", promo_codes)

    # Assert
    assert result == 30.0


def test_should_raise_error_when_subtotal_is_negative() -> None:
    # Arrange
    promo_codes = []

    # Act / Assert
    with pytest.raises(ValueError, match="Subtotal cannot be negative"):
        apply_promo_code(-1.0, "ANY", promo_codes)


def test_should_return_normal_multiplier_for_tuesday_15h() -> None:
    # Arrange
    hour, day = 15.0, "mardi"

    # Act
    result = calculate_surge(hour, day)

    # Assert
    assert result == 1.0


def test_should_return_lunch_multiplier_for_wednesday_12h30() -> None:
    # Arrange
    hour, day = 12.5, "mercredi"

    # Act
    result = calculate_surge(hour, day)

    # Assert
    assert result == 1.3


def test_should_return_dinner_multiplier_for_thursday_20h() -> None:
    # Arrange
    hour, day = 20.0, "jeudi"

    # Act
    result = calculate_surge(hour, day)

    # Assert
    assert result == 1.5


def test_should_return_weekend_evening_multiplier_for_friday_21h() -> None:
    # Arrange
    hour, day = 21.0, "vendredi"

    # Act
    result = calculate_surge(hour, day)

    # Assert
    assert result == 1.8


def test_should_return_sunday_multiplier_for_sunday_14h() -> None:
    # Arrange
    hour, day = 14.0, "dimanche"

    # Act
    result = calculate_surge(hour, day)

    # Assert
    assert result == 1.2


def test_should_return_normal_multiplier_at_11h30_boundary() -> None:
    # Arrange
    hour, day = 11.5, "mardi"

    # Act
    result = calculate_surge(hour, day)

    # Assert
    assert result == 1.0


def test_should_return_dinner_multiplier_at_19h00_boundary() -> None:
    # Arrange
    hour, day = 19.0, "jeudi"

    # Act
    result = calculate_surge(hour, day)

    # Assert
    assert result == 1.5


def test_should_return_weekend_evening_multiplier_at_22h00_boundary() -> None:
    # Arrange
    hour, day = 22.0, "vendredi"

    # Act
    result = calculate_surge(hour, day)

    # Assert
    assert result == 1.8


def test_should_return_closed_multiplier_before_opening() -> None:
    # Arrange
    hour, day = 9.59, "mercredi"

    # Act
    result = calculate_surge(hour, day)

    # Assert
    assert result == 0.0


def test_should_return_open_multiplier_at_10h00_boundary() -> None:
    # Arrange
    hour, day = 10.0, "lundi"

    # Act
    result = calculate_surge(hour, day)

    # Assert
    assert result == 1.0


def test_should_compute_full_order_total_without_promo_for_tuesday_15h() -> (
    None
):
    # Arrange
    items = [{"name": "Pizza", "price": 12.50, "quantity": 2}]

    # Act
    result = calculate_order_total(items, 5, 2, None, 15.0, "mardi")

    # Assert
    assert result["subtotal"] == 25.0
    assert result["discount"] == 0.0
    assert result["deliveryFee"] == 3.0
    assert result["surge"] == 1.0
    assert result["total"] == 28.0


def test_should_compute_full_order_total_with_20_percent_promo() -> None:
    # Arrange
    items = [{"name": "Pizza", "price": 12.50, "quantity": 2}]

    # Act
    result = calculate_order_total(
        items,
        5,
        2,
        "BIENVENUE20",
        15.0,
        "mardi",
    )

    # Assert
    assert result["subtotal"] == 25.0
    assert result["discount"] == 5.0
    assert result["deliveryFee"] == 3.0
    assert result["surge"] == 1.0
    assert result["total"] == 23.0


def test_should_apply_friday_evening_surge_only_to_delivery_fee() -> None:
    # Arrange
    items = [{"name": "Pizza", "price": 12.50, "quantity": 2}]

    # Act
    result = calculate_order_total(items, 5, 2, None, 20.0, "vendredi")

    # Assert
    assert result["subtotal"] == 25.0
    assert result["deliveryFee"] == 3.0
    assert result["surge"] == 1.8
    assert result["total"] == 30.4


def test_should_raise_error_when_items_are_empty() -> None:
    # Arrange
    items: list[dict[str, str | int | float]] = []

    # Act / Assert
    with pytest.raises(ValueError, match="Items cannot be empty"):
        calculate_order_total(items, 5, 2, None, 15.0, "mardi")


def test_should_ignore_item_when_quantity_is_zero() -> None:
    # Arrange
    items = [
        {"name": "Pizza", "price": 12.50, "quantity": 0},
        {"name": "Drink", "price": 5.00, "quantity": 1},
    ]

    # Act
    result = calculate_order_total(items, 5, 2, None, 15.0, "mardi")

    # Assert
    assert result["subtotal"] == 5.0
    assert result["total"] == 8.0


def test_should_raise_error_when_item_price_is_negative() -> None:
    # Arrange
    items = [{"name": "Pizza", "price": -1.0, "quantity": 1}]

    # Act / Assert
    with pytest.raises(ValueError, match="Item price cannot be negative"):
        calculate_order_total(items, 5, 2, None, 15.0, "mardi")


def test_should_raise_error_when_order_is_placed_after_opening_hours() -> None:
    # Arrange
    items = [{"name": "Pizza", "price": 12.50, "quantity": 1}]

    # Act / Assert
    with pytest.raises(ValueError, match="Store is closed"):
        calculate_order_total(items, 5, 2, None, 23.0, "mardi")


def test_should_raise_error_when_distance_is_out_of_delivery_area() -> None:
    # Arrange
    items = [{"name": "Pizza", "price": 12.50, "quantity": 1}]

    # Act / Assert
    with pytest.raises(ValueError, match="out of service area"):
        calculate_order_total(items, 15, 2, None, 15.0, "mardi")


def test_should_return_all_expected_keys_in_order_total_object() -> None:
    # Arrange
    items = [{"name": "Pizza", "price": 12.50, "quantity": 1}]

    # Act
    result = calculate_order_total(items, 5, 2, None, 15.0, "mardi")

    # Assert
    assert set(result.keys()) == {
        "subtotal",
        "discount",
        "deliveryFee",
        "surge",
        "total",
    }


def test_should_keep_two_decimals_for_returned_amounts() -> None:
    # Arrange
    items = [{"name": "Pizza", "price": 12.345, "quantity": 1}]

    # Act
    result = calculate_order_total(items, 3, 2, None, 15.0, "mardi")

    # Assert
    assert result["subtotal"] == 12.35
    assert result["discount"] == 0.0
    assert result["deliveryFee"] == 2.0
    assert result["total"] == 14.35


def test_should_match_subtotal_plus_delivery_without_promo() -> None:
    # Arrange
    items = [
        {"name": "Pizza", "price": 12.50, "quantity": 1},
        {"name": "Pasta", "price": 8.00, "quantity": 1},
    ]

    # Act
    result = calculate_order_total(items, 5, 2, None, 15.0, "mardi")

    # Assert
    assert result["discount"] == 0.0
    assert result["surge"] == 1.0
    assert result["total"] == round(
        result["subtotal"] + result["deliveryFee"],
        2,
    )
