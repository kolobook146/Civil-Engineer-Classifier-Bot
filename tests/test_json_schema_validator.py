from __future__ import annotations

from application.json_schema_validator import JsonSchemaValidator


def test_validator_accepts_non_null_stage_and_function() -> None:
    validator = JsonSchemaValidator()

    result = validator.validate(
        result_json=(
            '{"volume":1,"unit":null,"workType":null,'
            '"stage":"Execution","function":"Construction","comment":null}'
        )
    )

    assert result.is_valid is True
    assert result.errors == ()


def test_validator_rejects_null_stage() -> None:
    validator = JsonSchemaValidator()

    result = validator.validate(
        result_json=(
            '{"volume":1,"unit":null,"workType":null,'
            '"stage":null,"function":"Construction","comment":null}'
        )
    )

    assert result.is_valid is False
    assert result.errors == (
        "schema_validation_failed: None is not of type 'string'",
    )


def test_validator_rejects_null_function() -> None:
    validator = JsonSchemaValidator()

    result = validator.validate(
        result_json=(
            '{"volume":1,"unit":null,"workType":null,'
            '"stage":"Execution","function":null,"comment":null}'
        )
    )

    assert result.is_valid is False
    assert result.errors == (
        "schema_validation_failed: None is not of type 'string'",
    )
