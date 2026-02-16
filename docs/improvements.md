# Improvements Backlog

Цель: единый список улучшений для перехода от пилота к post-pilot версии.

## Правила ведения

- `priority`: `P0` (критично), `P1` (высокий), `P2` (средний), `P3` (низкий).
- `target_phase`: `pilot` или `post-pilot`.
- `status`: `planned`, `in_progress`, `done`, `rejected`.
- `owner`: роль или имя ответственного.

## Backlog

| id | idea | priority | target_phase | status | owner | notes |
|---|---|---|---|---|---|---|
| IMP-001 | Идемпотентная запись в Google Sheets по уникальному ключу сообщения (`chat_id + message_id`) | P1 | post-pilot | planned | TBD | Исключить дубли при повторной обработке |
| IMP-002 | Retry-политика очереди (1/5/15 минут) и DLQ | P1 | post-pilot | planned | TBD | Повысить надежность при временных сбоях LLM/Sheets |
| IMP-003 | Логирование confidence и причин пустых полей классификации | P2 | post-pilot | planned | TBD | Улучшение качества prompt и справочников |
| IMP-004 | Мониторинг: таймауты LLM, размер очереди, доля невалидных JSON, ошибки Sheets | P1 | post-pilot | planned | TBD | Метрики + алерты |
| IMP-005 | Расширение структуры справочников до полей `code`, `label`, `description` | P1 | post-pilot | planned | TBD | Сейчас используется только `label` |
| IMP-006 | Нормализация единиц измерения через отдельный справочник единиц и алиасов | P2 | post-pilot | planned | TBD | Сейчас вариативность оставляется LLM |
| IMP-007 | Дедупликация входящих сообщений по `chat_id + message_id` на уровне ingestion | P2 | post-pilot | planned | TBD | Отдельно от идемпотентности записи |
| IMP-008 | Роли доступа (кто может отправлять факты выполнения) | P2 | post-pilot | planned | TBD | На пилоте доступ открыт |
| IMP-009 | Редактирование/отмена ранее внесенной записи пользователем | P3 | post-pilot | planned | TBD | Нужен UX и модель версий |
| IMP-010 | Каталог синонимов/аббревиатур для справочников (`ОВиК`, `ВК`, `СМР`, `ПНР`, и т.д.) | P2 | post-pilot | planned | TBD | Повысить точность маппинга к `label` |
| IMP-011 | Обновить рабочее Python-окружение до `3.11` | P0 | pilot | planned | TBD | Нужно для совместимости проекта (например, `StrEnum`) |
| IMP-012 | Прогнать интеграционный smoke-test c реальными `GOOGLE_SERVICE_ACCOUNT_FILE` и `GOOGLE_SHEETS_SPREADSHEET_ID` | P0 | pilot | planned | TBD | Подтвердить запись в `data_facts` end-to-end |
| IMP-013 | Зафиксировать operational-режим пилота: очередь работает без retry/DLQ | P2 | pilot | planned | TBD | Осознанно оставляем упрощенный режим для аудитории ~5 пользователей |

## Ближайшие кандидаты в работу

1. `IMP-011` (обновление Python до `3.11`).
2. `IMP-012` (smoke-test записи в Google Sheets).
3. `IMP-005` (структура справочников `code/label/description`).
