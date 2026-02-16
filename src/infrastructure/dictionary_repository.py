from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Final

from config.settings import DictionarySettings

_COMMENT_PREFIXES: Final[tuple[str, ...]] = ("#", "//", ";")


@dataclass(frozen=True, slots=True)
class ClassificationDictionary:
    work_types: tuple[str, ...]
    stages: tuple[str, ...]
    functions: tuple[str, ...]
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
        version = self._build_version(
            self._settings.work_types_file,
            self._settings.stages_file,
            self._settings.functions_file,
        )

        return ClassificationDictionary(
            work_types=work_types,
            stages=stages,
            functions=functions,
            version=version,
        )

    def loadFromTextFiles(self) -> ClassificationDictionary:
        """Compatibility alias with UML naming."""
        return self.load_from_text_files()

    @staticmethod
    def _read_dictionary_values(path: Path) -> tuple[str, ...]:
        if not path.exists():
            raise FileNotFoundError(f"Dictionary file not found: {path}")

        values: list[str] = []
        seen: set[str] = set()
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            value = raw_line.strip()
            if not value or value.startswith(_COMMENT_PREFIXES):
                continue
            if value in seen:
                continue

            values.append(value)
            seen.add(value)

        return tuple(values)

    def _build_version(self, *paths: Path) -> str:
        digest = sha256()
        digest.update(self._base_version.encode("utf-8"))

        for path in paths:
            digest.update(path.as_posix().encode("utf-8"))
            digest.update(path.read_bytes())

        return f"{self._base_version}:{digest.hexdigest()[:12]}"
