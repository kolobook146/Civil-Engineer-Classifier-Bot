from __future__ import annotations


class CorrelationIdFactory:
    @staticmethod
    def build_trace_id(chat_id: str, message_id: str) -> str:
        return f"{chat_id}:{message_id}"
