from __future__ import annotations

from domain.models import ClassificationResult


class FallbackMapper:
    """Maps invalid LLM output to fallback classification payload."""

    @staticmethod
    def map_invalid(*, raw_llm_response: str) -> ClassificationResult:
        return ClassificationResult(
            volume=None,
            unit=None,
            work_type=None,
            stage=None,
            function=None,
            comment=raw_llm_response,
        )

    def mapInvalid(self, rawLlmResponse: str) -> ClassificationResult:
        """Compatibility alias with UML naming."""
        return self.map_invalid(raw_llm_response=rawLlmResponse)
