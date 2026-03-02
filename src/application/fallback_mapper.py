from __future__ import annotations

import re

from domain.models import ClassificationResult


class FallbackMapper:
    """Maps invalid LLM output to fallback classification payload."""

    _MAX_COMMENT_LENGTH = 2000
    _MAX_SECTION_LENGTH = 400
    _MAX_RAW_RESPONSE_PREVIEW_LENGTH = 1200

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
            errors_text = FallbackMapper._sanitize_text("; ".join(validation_errors))
            lines.append(
                "Validation errors: "
                f"{FallbackMapper._truncate(errors_text, FallbackMapper._MAX_SECTION_LENGTH)}"
            )
        if normalization_notes:
            notes_text = FallbackMapper._sanitize_text("; ".join(normalization_notes))
            lines.append(
                "Normalization notes: "
                f"{FallbackMapper._truncate(notes_text, FallbackMapper._MAX_SECTION_LENGTH)}"
            )

        lines.append("Raw LLM response preview:")
        stripped = FallbackMapper._sanitize_text(raw_llm_response)
        if not stripped:
            lines.append("<empty>")
        else:
            lines.append(
                FallbackMapper._truncate(
                    stripped,
                    FallbackMapper._MAX_RAW_RESPONSE_PREVIEW_LENGTH,
                )
            )

        return FallbackMapper._truncate(
            "\n".join(lines),
            FallbackMapper._MAX_COMMENT_LENGTH,
        )

    @staticmethod
    def _sanitize_text(text: str) -> str:
        normalized = text.replace("\r\n", "\n").replace("\r", "\n").replace("\t", " ")
        sanitized_chars = [
            char if (char == "\n" or char.isprintable()) else " "
            for char in normalized
        ]
        sanitized = "".join(sanitized_chars)
        compact_lines = [re.sub(r" {2,}", " ", line).strip() for line in sanitized.split("\n")]
        non_empty_lines = [line for line in compact_lines if line]
        return "\n".join(non_empty_lines).strip()

    @staticmethod
    def _truncate(text: str, max_length: int) -> str:
        if len(text) <= max_length:
            return text

        suffix = " ... [truncated]"
        cutoff = max(0, max_length - len(suffix))
        return text[:cutoff].rstrip() + suffix
