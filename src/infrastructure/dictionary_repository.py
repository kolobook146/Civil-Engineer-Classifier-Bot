from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Final, Iterator

from config.settings import DictionarySettings

_COMMENT_PREFIXES: Final[tuple[str, ...]] = ("#", "//", ";")


@dataclass(frozen=True, slots=True)
class ClassificationDictionary:
    work_types: tuple[str, ...]
    stages: tuple[str, ...]
    functions: tuple[str, ...]
    units: tuple[str, ...]
    unit_descriptions: dict[str, str]
    version: str


class DictionaryRepository:
    """Loads pilot dictionaries from local text files."""

    def __init__(self, settings: DictionarySettings, *, base_version: str = "pilot-v1") -> None:
        self._settings = settings
        self._base_version = base_version

    def load_from_text_files(self) -> ClassificationDictionary:
        work_types = self._read_dictionary_values(self._settings.work_types_file)
        stages = self._read_dictionary_values(self._settings.stages_file)
        functions = self._read_dictionary_values(self._settings.functions_file)
        units, unit_descriptions = self._read_dictionary_values_with_descriptions(
            self._settings.units_file
        )
        version = self._build_version(
            self._settings.work_types_file,
            self._settings.stages_file,
            self._settings.functions_file,
            self._settings.units_file,
        )

        return ClassificationDictionary(
            work_types=work_types,
            stages=stages,
            functions=functions,
            units=units,
            unit_descriptions=unit_descriptions,
            version=version,
        )

    def loadFromTextFiles(self) -> ClassificationDictionary:
        """Compatibility alias with UML naming."""
        return self.load_from_text_files()

    def preflight_check(self) -> ClassificationDictionary:
        dictionary = self.load_from_text_files()

        if not dictionary.work_types:
            raise RuntimeError("work types dictionary is empty")
        if not dictionary.stages:
            raise RuntimeError("stages dictionary is empty")
        if not dictionary.functions:
            raise RuntimeError("functions dictionary is empty")
        if not dictionary.units:
            raise RuntimeError("units dictionary is empty")

        return dictionary

    @staticmethod
    def _read_dictionary_values(path: Path) -> tuple[str, ...]:
        values, _ = DictionaryRepository._read_dictionary_values_with_descriptions(path)
        return values

    @staticmethod
    def _read_dictionary_values_with_descriptions(path: Path) -> tuple[tuple[str, ...], dict[str, str]]:
        if not path.exists():
            raise FileNotFoundError(f"Dictionary file not found: {path}")

        values: list[str] = []
        seen: set[str] = set()
        descriptions: dict[str, str] = {}
        for value, description in DictionaryRepository._iter_dictionary_rows(path):
            if value in seen:
                continue
            values.append(value)
            seen.add(value)
            if description:
                descriptions[value] = description

        return tuple(values), descriptions

    @staticmethod
    def _iter_dictionary_rows(path: Path) -> Iterator[tuple[str, str | None]]:
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            parsed = DictionaryRepository._parse_dictionary_line(raw_line)
            if parsed is None:
                continue
            yield parsed

    @staticmethod
    def _parse_dictionary_line(raw_line: str) -> tuple[str, str | None] | None:
        stripped = raw_line.strip()
        if not stripped or stripped.startswith(_COMMENT_PREFIXES):
            return None

        columns = [column.strip() for column in raw_line.split("\t")]
        lowered = tuple(column.lower() for column in columns)

        if lowered[:2] in {
            ("unit", "description"),
            ("label", "description"),
            ("единица", "описание"),
        }:
            return None
        if lowered[:3] in {
            ("code", "label", "description"),
            ("код", "наименование", "описание"),
            ("код", "label", "description"),
        }:
            return None

        value: str
        description: str | None
        if len(columns) >= 3:
            value = columns[1] or columns[0]
            description = columns[2] or None
        elif len(columns) == 2:
            value = columns[0]
            description = columns[1] or None
        else:
            value = columns[0]
            description = None

        value = value.strip()
        if not value or value.startswith(_COMMENT_PREFIXES):
            return None

        return value, description

    def _build_version(self, *paths: Path) -> str:
        digest = sha256()
        digest.update(self._base_version.encode("utf-8"))

        for path in paths:
            digest.update(path.as_posix().encode("utf-8"))
            digest.update(path.read_bytes())

        return f"{self._base_version}:{digest.hexdigest()[:12]}"
