from __future__ import annotations


class MessagePreprocessor:
    """Input text normalization for pilot message handling."""

    def normalize(self, text: str) -> str:
        return " ".join(text.strip().split())
