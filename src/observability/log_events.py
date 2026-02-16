from __future__ import annotations

from enum import StrEnum


class LogEvent(StrEnum):
    polling_started = "polling_started"
    queue_worker_bootstrap_started = "queue_worker_bootstrap_started"
    queue_worker_started = "queue_worker_started"
    message_received = "message_received"
    llm_response_received = "llm_response_received"
    llm_timeout = "llm_timeout"
    json_validation_passed = "json_validation_passed"
    json_validation_failed = "json_validation_failed"
    queue_enqueued = "queue_enqueued"
    queue_enqueue_failed = "queue_enqueue_failed"
    queue_dequeued = "queue_dequeued"
    queue_task_invalid = "queue_task_invalid"
    queue_processing_failed = "queue_processing_failed"
    sheets_write_success = "sheets_write_success"
    sheets_write_failed = "sheets_write_failed"
    post_factum_notification_sent = "post_factum_notification_sent"
    classification_failed = "classification_failed"
    telegram_update_error = "telegram_update_error"
