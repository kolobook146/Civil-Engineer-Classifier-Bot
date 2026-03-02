from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Final

from infrastructure.dictionary_repository import ClassificationDictionary

from .decimal_volume import decimal_to_json_number, decimal_to_string, parse_decimal_volume
from .unit_key_normalizer import normalize_unit_key

_CLASSIFICATION_FIELDS: Final[tuple[str, ...]] = (
    "volume",
    "unit",
    "workType",
    "stage",
    "function",
    "comment",
)


@dataclass(frozen=True, slots=True)
class PayloadNormalizationResult:
    normalized_json: str
    notes: tuple[str, ...]


class LLMPayloadNormalizer:
    """Normalizes LLM JSON payload into pilot-compatible scalar fields."""

    def normalize(
        self,
        *,
        result_json: str,
        dictionary: ClassificationDictionary | None = None,
    ) -> PayloadNormalizationResult:
        try:
            raw_payload = json.loads(result_json)
        except json.JSONDecodeError:
            return PayloadNormalizationResult(
                normalized_json=result_json,
                notes=(),
            )

        if not isinstance(raw_payload, dict):
            return PayloadNormalizationResult(
                normalized_json=result_json,
                notes=("root_not_object",),
            )

        normalized_payload: dict[str, Any] = dict(raw_payload)
        notes: list[str] = []

        for field in _CLASSIFICATION_FIELDS:
            if field not in raw_payload:
                continue
            value = raw_payload.get(field)
            normalized_value, field_notes = self._normalize_field(
                field=field,
                value=value,
                dictionary=dictionary,
            )
            normalized_payload[field] = normalized_value
            notes.extend(field_notes)

        normalized_json = json.dumps(
            normalized_payload,
            ensure_ascii=False,
            separators=(",", ":"),
        )
        return PayloadNormalizationResult(
            normalized_json=normalized_json,
            notes=tuple(notes),
        )

    def _normalize_field(
        self,
        *,
        field: str,
        value: Any,
        dictionary: ClassificationDictionary | None,
    ) -> tuple[Any, tuple[str, ...]]:
        if field == "volume":
            return self._normalize_volume(value)
        if field == "comment":
            return self._normalize_comment(value)
        if field == "unit":
            return self._normalize_unit(value=value, dictionary=dictionary)
        return self._normalize_categorical(field=field, value=value)

    def _normalize_volume(self, value: Any) -> tuple[int | float | None, tuple[str, ...]]:
        if value is None:
            return None, ()

        decimal_value = parse_decimal_volume(value)
        if decimal_value is not None:
            normalized_value = decimal_to_json_number(decimal_value)
            if isinstance(value, str):
                stripped = value.strip().replace("\u00a0", "").replace(" ", "")
                if stripped != decimal_to_string(decimal_value):
                    return normalized_value, ("volume_string_normalized_to_decimal_number",)
                return normalized_value, ()
            if isinstance(value, (int, float)):
                return normalized_value, ("volume_number_normalized_to_decimal_number",)
            return normalized_value, ("volume_normalized_to_decimal_number",)

        if isinstance(value, bool):
            return None, ("volume_bool_to_null",)
        if isinstance(value, str):
            return None, ("volume_unparseable_to_null",)
        if isinstance(value, dict):
            candidate = self._extract_from_single_pair(value, prefer_key=False)
            if candidate is None:
                return None, ("volume_object_to_null",)
            decimal_candidate = parse_decimal_volume(candidate)
            if decimal_candidate is None:
                return None, ("volume_object_unparseable_to_null",)
            return decimal_to_json_number(decimal_candidate), ("volume_object_to_decimal_number",)
        if isinstance(value, (list, tuple)):
            candidate = self._extract_from_single_item_list(value, prefer_key=False)
            if candidate is None:
                return None, ("volume_list_to_null",)
            decimal_candidate = parse_decimal_volume(candidate)
            if decimal_candidate is None:
                return None, ("volume_list_unparseable_to_null",)
            return decimal_to_json_number(decimal_candidate), ("volume_list_to_decimal_number",)
        return None, ("volume_unsupported_to_null",)

    def _normalize_categorical(self, *, field: str, value: Any) -> tuple[str | None, tuple[str, ...]]:
        if value is None:
            return None, ()
        if isinstance(value, str):
            normalized = value.strip()
            if not normalized:
                return None, (f"{field}_empty_to_null",)
            return normalized, ()
        if isinstance(value, bool):
            return None, (f"{field}_bool_to_null",)
        if isinstance(value, (int, float)):
            return str(value), (f"{field}_number_to_string",)
        if isinstance(value, dict):
            candidate = self._extract_from_single_pair(value, prefer_key=True)
            if candidate is None:
                return None, (f"{field}_object_to_null",)
            return candidate, (f"{field}_object_to_string",)
        if isinstance(value, (list, tuple)):
            candidate = self._extract_from_single_item_list(value, prefer_key=True)
            if candidate is None:
                return None, (f"{field}_list_to_null",)
            return candidate, (f"{field}_list_to_string",)
        return None, (f"{field}_unsupported_to_null",)

    def _normalize_unit(
        self,
        *,
        value: Any,
        dictionary: ClassificationDictionary | None,
    ) -> tuple[str | None, tuple[str, ...]]:
        normalized_value, notes = self._normalize_categorical(field="unit", value=value)
        if normalized_value is None or dictionary is None:
            return normalized_value, notes

        canonical_unit = normalize_unit_key(normalized_value, dictionary.units)
        if canonical_unit is None:
            return normalized_value, notes
        if canonical_unit == normalized_value:
            return normalized_value, notes
        return canonical_unit, (*notes, "unit_canonicalized_to_dictionary_key")

    @staticmethod
    def _normalize_comment(value: Any) -> tuple[str | None, tuple[str, ...]]:
        if value is None:
            return None, ()
        if isinstance(value, str):
            normalized = value.strip()
            if not normalized:
                return None, ("comment_empty_to_null",)
            return normalized, ()
        if isinstance(value, bool):
            return str(value).lower(), ("comment_bool_to_string",)
        if isinstance(value, (int, float)):
            return str(value), ("comment_number_to_string",)
        if isinstance(value, (dict, list, tuple)):
            compact = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
            return compact, ("comment_object_to_string",)
        return str(value), ("comment_unsupported_to_string",)

    @staticmethod
    def _extract_from_single_pair(value: dict[Any, Any], *, prefer_key: bool) -> str | None:
        if len(value) != 1:
            return None

        key, sub_value = next(iter(value.items()))
        key_text = LLMPayloadNormalizer._scalar_to_string(key)
        sub_value_text = LLMPayloadNormalizer._scalar_to_string(sub_value)

        if prefer_key and key_text is not None:
            return key_text
        if sub_value_text is not None:
            return sub_value_text
        if key_text is not None:
            return key_text
        return None

    @staticmethod
    def _extract_from_single_item_list(value: list[Any] | tuple[Any, ...], *, prefer_key: bool) -> str | None:
        if len(value) != 1:
            return None

        item = value[0]
        if isinstance(item, dict):
            return LLMPayloadNormalizer._extract_from_single_pair(item, prefer_key=prefer_key)
        return LLMPayloadNormalizer._scalar_to_string(item)

    @staticmethod
    def _scalar_to_string(value: Any) -> str | None:
        if isinstance(value, bool):
            return None
        if isinstance(value, (int, float)):
            return str(value)
        if isinstance(value, str):
            normalized = value.strip()
            if normalized:
                return normalized
        return None
