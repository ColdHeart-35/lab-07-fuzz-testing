"""Property-based fuzz tests for processor.py (run with pytest)."""

import math

from hypothesis import given, strategies as st

from processor import calculate_average, normalize_username, parse_int_list


@given(st.one_of(st.text(), st.none(), st.integers(), st.lists(st.integers())))
def test_parse_int_list_never_crashes(value):
    result = parse_int_list(value)
    assert isinstance(result, list)
    assert all(type(item) is int for item in result)


@given(st.lists(st.integers(min_value=-(10**30), max_value=10**30), max_size=100))
def test_parse_int_list_round_trip(values):
    encoded = ",".join(map(str, values))
    assert parse_int_list(encoded) == values


@given(st.one_of(st.text(), st.none(), st.integers(), st.lists(st.text())))
def test_normalize_username_never_crashes(value):
    result = normalize_username(value)
    assert isinstance(result, str)
    assert len(result) <= 32
    assert all(char in "abcdefghijklmnopqrstuvwxyz0123456789_-" for char in result)


@given(st.text(alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-", min_size=1, max_size=32))
def test_normalize_username_is_lowercase_and_idempotent(value):
    normalized = normalize_username(value)
    assert normalized == value.lower()
    assert normalize_username(normalized) == normalized


@given(st.one_of(st.lists(st.one_of(st.integers(), st.floats(allow_nan=True, allow_infinity=True)), max_size=100), st.none(), st.text()))
def test_calculate_average_never_crashes(value):
    result = calculate_average(value)
    assert result is None or (isinstance(result, float) and math.isfinite(result))


@given(st.lists(st.floats(allow_nan=False, allow_infinity=False, width=32), min_size=1, max_size=100))
def test_average_of_finite_numbers_is_between_extrema(values):
    result = calculate_average(values)
    assert result is not None
    assert min(values) <= result <= max(values)


def test_known_invalid_inputs_are_handled():
    assert parse_int_list("1,,oops") == []
    assert parse_int_list(None) == []
    assert normalize_username("../admin") == ""
    assert normalize_username(None) == ""
    assert calculate_average([]) is None
    assert calculate_average([1, float("nan")]) is None
