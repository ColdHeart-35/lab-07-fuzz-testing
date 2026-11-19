"""Small input-processing examples hardened for fuzz testing."""

from math import isfinite
import re
from typing import Optional


def parse_int_list(value: object) -> list[int]:
    """Parse comma-separated decimal integers; return [] for invalid input.

    Empty fields are ignored (so ``"1,,2"`` becomes ``[1, 2]``). Non-string
    inputs and fields that are not integers make the whole input invalid.
    """
    if not isinstance(value, str):
        return []
    try:
        parts = value.split(",")
        if len(parts) > 10_000:
            return []
        result = []
        for part in parts:
            part = part.strip()
            if not part:
                continue
            # Bound conversion work and avoid accepting non-decimal forms.
            if len(part) > 128 or not re.fullmatch(r"[+-]?\d+", part):
                return []
            result.append(int(part, 10))
        return result
    except (ValueError, OverflowError):
        return []


def normalize_username(value: object) -> str:
    """Normalize a username to lowercase ASCII letters, digits, '_' or '-'."""
    if not isinstance(value, str) or len(value) > 256:
        return ""
    normalized = value.strip().lower()
    if not 1 <= len(normalized) <= 32:
        return ""
    if not re.fullmatch(r"[a-z0-9_-]+", normalized):
        return ""
    return normalized


def calculate_average(values: object) -> Optional[float]:
    """Return the finite numeric average, or None for invalid/empty input."""
    if not isinstance(values, (list, tuple)) or not values or len(values) > 10_000:
        return None
    numbers = []
    for value in values:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return None
        try:
            number = float(value)
        except (ValueError, OverflowError):
            return None
        if not isfinite(number):
            return None
        numbers.append(number)
    # Scale to avoid overflow while retaining precision for tiny magnitudes.
    scale = max(abs(number) for number in numbers)
    if scale == 0:
        return 0.0
    average = (sum(number / scale for number in numbers) / len(numbers)) * scale
    return average if isfinite(average) else None


if __name__ == "__main__":
    print("parse_int_list('10, 20,30'):", parse_int_list("10, 20,30"))
    print("normalize_username('  Alice_01  '):", normalize_username("  Alice_01  "))
    print("calculate_average([10, 20, 30]):", calculate_average([10, 20, 30]))
    print("parse_int_list('1,,oops'):", parse_int_list("1,,oops"))
    print("normalize_username(None):", repr(normalize_username(None)))
    print("calculate_average([]):", calculate_average([]))
