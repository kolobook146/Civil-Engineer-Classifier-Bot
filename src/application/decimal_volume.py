from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation
from typing import Any

_VALID_DECIMAL_RE = re.compile(r"^[+-]?\d+(?:\.\d+)?$")


def parse_decimal_volume(value: Any) -> Decimal | None:
    if value is None:
        return None

    if isinstance(value, bool):
        return None

    if isinstance(value, Decimal):
        return value

    if isinstance(value, int):
        return Decimal(value)

    if isinstance(value, float):
        try:
            return Decimal(str(value))
        except InvalidOperation:
            return None

    if isinstance(value, str):
        normalized = _normalize_decimal_string(value)
        if normalized is None:
            return None
        try:
            return Decimal(normalized)
        except InvalidOperation:
            return None

    return None


def decimal_to_string(value: Decimal) -> str:
    text = format(value, "f")
    if "." not in text:
        return text
    return text.rstrip("0").rstrip(".")


def decimal_to_json_number(value: Decimal) -> int | float:
    if value == value.to_integral_value():
        return int(value)
    return float(value)


def _normalize_decimal_string(raw: str) -> str | None:
    candidate = raw.strip()
    if not candidate:
        return None

    candidate = candidate.replace("\u00a0", "").replace(" ", "")
    if not candidate:
        return None

    comma_count = candidate.count(",")
    dot_count = candidate.count(".")

    if comma_count > 0 and dot_count > 0:
        last_comma = candidate.rfind(",")
        last_dot = candidate.rfind(".")
        if last_comma > last_dot:
            candidate = candidate.replace(".", "")
            candidate = candidate.replace(",", ".")
        else:
            candidate = candidate.replace(",", "")
    elif comma_count > 0:
        candidate = _normalize_single_separator(candidate, ",")
        if candidate is None:
            return None
    elif dot_count > 0:
        candidate = _normalize_single_separator(candidate, ".")
        if candidate is None:
            return None

    if not _VALID_DECIMAL_RE.fullmatch(candidate):
        return None
    return candidate


def _normalize_single_separator(candidate: str, separator: str) -> str | None:
    parts = candidate.split(separator)

    if len(parts) == 2:
        left, right = parts
        if not left or not right:
            return None
        if not _digits_with_optional_sign(left):
            return None
        if not right.isdigit():
            return None
        return f"{left}.{right}" if separator == "," else candidate

    if len(parts) > 2:
        sign = ""
        first = parts[0]
        if first.startswith(("+", "-")):
            sign = first[0]
            first = first[1:]

        if not first.isdigit() or not all(part.isdigit() for part in parts[1:]):
            return None

        if all(len(part) == 3 for part in parts[1:]):
            joined = first + "".join(parts[1:])
            return f"{sign}{joined}"

        whole = first + "".join(parts[1:-1])
        fractional = parts[-1]
        if not whole or not fractional:
            return None
        if not whole.isdigit() or not fractional.isdigit():
            return None
        return f"{sign}{whole}.{fractional}"

    return None


def _digits_with_optional_sign(value: str) -> bool:
    if value.startswith(("+", "-")):
        return value[1:].isdigit() and len(value) > 1
    return value.isdigit()
