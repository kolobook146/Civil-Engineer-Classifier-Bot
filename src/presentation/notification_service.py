from __future__ import annotations

import json

from observability.correlation_id_factory import CorrelationIdFactory
from observability.log_context import LogContext
from observability.log_events import LogEvent
from observability.logging_service import LoggingService
from telegram import Bot, InlineKeyboardMarkup, Message


class NotificationService:
    """Outbound user messages for Telegram interactions."""

    def __init__(
        self,
        *,
        logging_service: LoggingService,
        correlation_id_factory: CorrelationIdFactory,
    ) -> None:
        self._logging_service = logging_service
        self._correlation_id_factory = correlation_id_factory
        self._welcome_text = (
            "Привет! Я бот учета выполненных работ по строительному проекту. "
            "Отправляйте факт выполнения в свободной форме, а я выделю объем, единицы, "
            "вид работ, стадию, функцию и комментарий, затем внесу запись в таблицу. "
            "Нажмите «Сообщить выполнение», чтобы начать."
        )
        self._input_instruction_text = (
            "Опишите выполненные работы одним сообщением в свободной форме. "
            "Пример: «Сделали двадцать кубов бетона, стадия монолит, функция генподряд, "
            "комментарий: оси 3-5». Можно писать числа словами и разговорные единицы — я нормализую."
        )

    async def send_welcome(
        self,
        *,
        target_message: Message,
        reply_markup: InlineKeyboardMarkup,
    ) -> None:
        await target_message.reply_text(
            text=self._welcome_text,
            reply_markup=reply_markup,
        )

    async def send_input_instruction(self, *, target_message: Message) -> None:
        await target_message.reply_text(self._input_instruction_text)

    async def send_immediate_confirmation(
        self,
        *,
        target_message: Message,
        classification_payload: dict[str, str | None],
        status: str,
    ) -> None:
        formatted_payload = json.dumps(classification_payload, ensure_ascii=False)
        await target_message.reply_text(
            f"Внесли данные: {formatted_payload}\n"
            f"Статус: {status}"
        )

    async def send_processing_error(self, *, target_message: Message) -> None:
        await target_message.reply_text(
            "Не удалось обработать сообщение. Попробуйте отправить его ещё раз."
        )

    async def send_queued_notice(self, *, target_message: Message) -> None:
        await target_message.reply_text(
            "ЛЛМ занята, сообщение в очереди, как запишем - сообщим."
        )

    async def send_post_factum_notification(
        self,
        *,
        bot: Bot,
        chat_id: str,
        user_id: str,
        message_id: str,
        classification_payload: dict[str, str | None],
        status: str,
    ) -> None:
        formatted_payload = json.dumps(classification_payload, ensure_ascii=False)
        chat_ref: int | str = int(chat_id) if chat_id.lstrip("-").isdigit() else chat_id
        await bot.send_message(
            chat_id=chat_ref,
            text=(
                "Сообщение из очереди внесено.\n"
                f"Внесли данные: {formatted_payload}\n"
                f"Статус: {status}"
            ),
        )
        self._logging_service.info(
            event=LogEvent.post_factum_notification_sent,
            component="notification_service",
            context=LogContext(
                trace_id=self._correlation_id_factory.build_trace_id(chat_id, message_id),
                chat_id=chat_id,
                user_id=user_id,
                message_id=message_id,
                processing_path="queue",
                status=status,
            ),
        )
