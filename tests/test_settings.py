from __future__ import annotations

from config.settings import load_settings


def test_startup_preflight_disabled_by_default(monkeypatch) -> None:
    monkeypatch.delenv("STARTUP_PREFLIGHT_ENABLED", raising=False)

    settings = load_settings()

    assert settings.app.startup_preflight_enabled is False


def test_startup_preflight_can_be_enabled_from_env(monkeypatch) -> None:
    monkeypatch.setenv("STARTUP_PREFLIGHT_ENABLED", "true")

    settings = load_settings()

    assert settings.app.startup_preflight_enabled is True
