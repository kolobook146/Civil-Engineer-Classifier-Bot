from __future__ import annotations

from typing import Final

_UNIT_ALIASES: Final[dict[str, str]] = {
    "%": "%",
    "г": "g",
    "гр": "g",
    "кг": "kg",
    "т": "t",
    "мм": "mm",
    "см": "cm",
    "дм": "dm",
    "м": "m",
    "м.п.": "m",
    "мп": "m",
    "п.м.": "m",
    "пм": "m",
    "пог.м.": "m",
    "погм": "m",
    "км": "km",
    "мм2": "mm2",
    "мм²": "mm2",
    "см2": "cm2",
    "см²": "cm2",
    "дм2": "dm2",
    "дм²": "dm2",
    "м2": "m2",
    "м²": "m2",
    "км2": "km2",
    "км²": "km2",
    "га": "ha",
    "см3": "cm3",
    "см³": "cm3",
    "дм3": "dm3",
    "дм³": "dm3",
    "л": "l",
    "мл": "ml",
    "м3": "m3",
    "м³": "m3",
    "куб": "m3",
    "куба": "m3",
    "кубов": "m3",
    "шт": "pcs",
    "шт.": "pcs",
    "ед": "unit",
    "ед.": "unit",
    "пара": "pair",
    "компл": "set",
    "компл.": "set",
    "комплект": "set",
    "узел": "node",
    "система": "system",
    "стык": "joint",
    "соединение": "connection",
    "звено": "link",
    "блок": "block",
    "панель": "panel",
    "плита": "slab",
    "лист": "sheet",
    "рулон": "roll",
    "решетка": "grille",
    "решётка": "grille",
    "линия": "line",
    "контур": "contour",
    "точка": "point",
    "отверстие": "opening",
    "скважина": "borehole",
    "элемент": "element",
    "изделие": "item",
    "устройство": "device",
    "в": "V",
    "а": "A",
    "квт": "kW",
    "ква": "kVA",
}


def normalize_unit_key(value: str, dictionary_units: tuple[str, ...]) -> str | None:
    raw_value = value.strip()
    if not raw_value:
        return None

    if raw_value in dictionary_units:
        return raw_value

    normalized = _normalize_unit_candidate(raw_value)
    if normalized in dictionary_units:
        return normalized

    lowered = normalized.lower()
    alias_hit = _UNIT_ALIASES.get(normalized)
    if alias_hit is None:
        alias_hit = _UNIT_ALIASES.get(lowered)
    if alias_hit is not None and alias_hit in dictionary_units:
        return alias_hit

    case_matches = [item for item in dictionary_units if item.lower() == lowered]
    if len(case_matches) == 1:
        return case_matches[0]

    return None


def _normalize_unit_candidate(value: str) -> str:
    normalized = value.strip().replace("\u00a0", " ")
    normalized = "".join(normalized.split())
    normalized = normalized.replace("²", "2").replace("³", "3")

    if normalized.endswith(".") and normalized not in {"%"}:
        normalized = normalized[:-1]

    return normalized
