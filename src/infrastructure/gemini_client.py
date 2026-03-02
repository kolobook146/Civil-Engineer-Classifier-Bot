from __future__ import annotations

from typing import Final

from google import genai
from google.genai import types

try:
    from google.api_core.exceptions import DeadlineExceeded
except Exception:  # pragma: no cover - optional dependency path
    DeadlineExceeded = None


_TIMEOUT_MARKERS: Final[tuple[str, ...]] = (
    "deadline exceeded",
    "timed out",
    "timeout",
    "time out",
)


class LLMTimeoutError(RuntimeError):
    """Raised when Gemini call exceeded timeout and should be queued."""


class GeminiClient:
    """Thin wrapper over google-genai for structured classification calls."""

    def __init__(
        self,
        *,
        api_key: str,
        model: str,
        timeout_seconds: int = 30,
        base_url: str = "",
    ) -> None:
        if not api_key:
            raise ValueError("api_key is required")
        if not model:
            raise ValueError("model is required")

        self._model = model
        self._timeout_seconds = timeout_seconds

        normalized_base_url = base_url.strip()
        if normalized_base_url and "/openai/" in normalized_base_url:
            raise ValueError(
                "LLM_BASE_URL points to OpenAI-compatible endpoint. "
                "For native google-genai, keep LLM_BASE_URL empty "
                "or use https://generativelanguage.googleapis.com/"
            )

        if normalized_base_url:
            self._client = genai.Client(
                api_key=api_key,
                http_options=types.HttpOptions(base_url=normalized_base_url),
            )
        else:
            self._client = genai.Client(api_key=api_key)

    def classify(self, prompt: str, timeout_seconds: int = 30) -> str:
        if not prompt.strip():
            raise ValueError("prompt must not be empty")

        effective_timeout_seconds = timeout_seconds or self._timeout_seconds
        # google-genai HttpOptions.timeout is milliseconds.
        effective_timeout_ms = max(1, int(effective_timeout_seconds * 1000))

        try:
            response = self._client.models.generate_content(
                model=self._model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    http_options=types.HttpOptions(timeout=effective_timeout_ms),
                ),
            )
        except Exception as exc:
            if self._is_timeout_exception(exc):
                raise LLMTimeoutError("Gemini request timed out") from exc
            raise

        text = self._extract_text(response)
        if not text:
            raise RuntimeError("Gemini returned empty response")

        return text.strip()

    def preflight_check(self, *, timeout_seconds: int | None = None) -> dict[str, int | str]:
        effective_timeout_seconds = timeout_seconds or min(5, self._timeout_seconds)
        response = self.classify(
            'Return exactly this JSON object and nothing else: {"ok": true}',
            timeout_seconds=effective_timeout_seconds,
        )
        return {
            "llm_model": self._model,
            "llm_preflight_timeout_seconds": effective_timeout_seconds,
            "llm_preflight_response_length": len(response),
        }

    def _extract_text(self, response: object) -> str:
        text = getattr(response, "text", None)
        if isinstance(text, str) and text.strip():
            return text

        candidates = getattr(response, "candidates", None)
        if not candidates:
            return ""

        parts_text: list[str] = []
        for candidate in candidates:
            content = getattr(candidate, "content", None)
            if content is None:
                continue

            parts = getattr(content, "parts", None) or []
            for part in parts:
                part_text = getattr(part, "text", None)
                if isinstance(part_text, str) and part_text.strip():
                    parts_text.append(part_text)

        return "\n".join(parts_text)

    def _is_timeout_exception(self, exc: Exception) -> bool:
        current: Exception | None = exc
        while current is not None:
            if isinstance(current, TimeoutError):
                return True
            if DeadlineExceeded is not None and isinstance(current, DeadlineExceeded):
                return True

            message = str(current).lower()
            if any(marker in message for marker in _TIMEOUT_MARKERS):
                return True

            next_exc = current.__cause__ if isinstance(current.__cause__, Exception) else None
            if next_exc is None and isinstance(current.__context__, Exception):
                next_exc = current.__context__
            current = next_exc

        return False
