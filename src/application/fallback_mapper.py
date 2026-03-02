from __future__ import annotations

from domain.models import ClassificationResult


class FallbackMapper:
    """Maps invalid LLM output to fallback classification payload."""

    @staticmethod
    def map_invalid(
        *,
        raw_llm_response: str,
        validation_errors: tuple[str, ...] | None = None,
        normalization_notes: tuple[str, ...] | None = None,
    ) -> ClassificationResult:
        comment = FallbackMapper._build_comment(
            raw_llm_response=raw_llm_response,
            validation_errors=validation_errors or (),
            normalization_notes=normalization_notes or (),
        )
        return ClassificationResult(
            volume=None,
            unit=None,
            work_type=None,
            stage=None,
            function=None,
            comment=comment,
        )

    def mapInvalid(self, rawLlmResponse: str) -> ClassificationResult:
        """Compatibility alias with UML naming."""
        return self.map_invalid(raw_llm_response=rawLlmResponse)

    @staticmethod
    def _build_comment(
        *,
        raw_llm_response: str,
        validation_errors: tuple[str, ...],
        normalization_notes: tuple[str, ...],
    ) -> str:
        lines: list[str] = [
            "Fallback applied: LLM payload failed strict validation.",
        ]
        if validation_errors:
            lines.append(f"Validation errors: {'; '.join(validation_errors)}")
        if normalization_notes:
            lines.append(f"Normalization notes: {'; '.join(normalization_notes)}")

        lines.append("Raw LLM response:")
        stripped = raw_llm_response.strip()
        lines.append(stripped if stripped else "<empty>")
        return "\n".join(lines)
