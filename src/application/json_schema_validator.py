from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jsonschema import ValidationError, validate

from infrastructure.dictionary_repository import ClassificationDictionary


@dataclass(frozen=True, slots=True)
class ValidationResult:
    is_valid: bool
    errors: tuple[str, ...]
    payload: dict[str, Any]


class JsonSchemaValidator:
    """Validates Gemini JSON against strict schema and dictionaries."""

    def __init__(self, schema_path: Path | None = None) -> None:
        self._schema_path = schema_path or self._default_schema_path()
        self._schema = self._load_schema(self._schema_path)

    @staticmethod
    def _default_schema_path() -> Path:
        return Path(__file__).resolve().parents[2] / "schemas" / "classification_result.schema.json"

    @staticmethod
    def _load_schema(path: Path) -> dict[str, Any]:
        if not path.exists():
            raise FileNotFoundError(f"JSON schema file not found: {path}")

        raw_schema = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(raw_schema, dict):
            raise RuntimeError("JSON schema root must be object")

        return raw_schema

    def validate(
        self,
        *,
        result_json: str,
        dictionary: ClassificationDictionary | None = None,
    ) -> ValidationResult:
        errors: list[str] = []
        try:
            raw_payload = json.loads(result_json)
        except json.JSONDecodeError as exc:
            return ValidationResult(
                is_valid=False,
                errors=(f"invalid_json: {exc.msg}",),
                payload={},
            )

        if not isinstance(raw_payload, dict):
            return ValidationResult(
                is_valid=False,
                errors=("schema_validation_failed: root must be JSON object",),
                payload={},
            )
        payload: dict[str, Any] = raw_payload

        try:
            validate(instance=payload, schema=self._schema)
        except ValidationError as exc:
            return ValidationResult(
                is_valid=False,
                errors=(f"schema_validation_failed: {exc.message}",),
                payload=payload,
            )

        if dictionary is not None:
            work_type = payload.get("workType")
            stage = payload.get("stage")
            function = payload.get("function")

            if work_type is not None and work_type not in dictionary.work_types:
                errors.append("workType_not_in_dictionary")
            if stage is not None and stage not in dictionary.stages:
                errors.append("stage_not_in_dictionary")
            if function is not None and function not in dictionary.functions:
                errors.append("function_not_in_dictionary")

        return ValidationResult(
            is_valid=not errors,
            errors=tuple(errors),
            payload=payload,
        )
