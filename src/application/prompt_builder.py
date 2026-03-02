from __future__ import annotations

from infrastructure.dictionary_repository import ClassificationDictionary


class PromptBuilder:
    """Builds a pilot classification prompt for Gemini."""

    def build(self, *, raw_text: str, dictionary: ClassificationDictionary) -> str:
        work_types = "\n".join(f"- {item}" for item in dictionary.work_types)
        stages = "\n".join(f"- {item}" for item in dictionary.stages)
        functions = "\n".join(f"- {item}" for item in dictionary.functions)
        units = "\n".join(
            self._format_unit_line(item, dictionary.unit_descriptions.get(item))
            for item in dictionary.units
        )

        return (
            "You are a classifier of construction project progress facts.\n"
            "Return JSON only, without markdown and without explanations.\n"
            "JSON fields: volume, unit, workType, stage, function, comment.\n"
            "For volume, return a JSON decimal number or null (use dot as decimal separator).\n"
            "For unit, return exactly one canonical ASCII unit key from the unit dictionary (left side before ':') or null.\n"
            "Do not return Russian unit abbreviations if an ASCII dictionary key exists.\n"
            "For workType, stage, and function, only one dictionary value or null is allowed.\n"
            "If a field is missing in the message, return null.\n"
            f"{self.build_stage_function_hint()}\n"
            "\n"
            "Unit dictionary:\n"
            f"{units}\n"
            "\n"
            "Work type dictionary:\n"
            f"{work_types}\n"
            "\n"
            "Stage dictionary:\n"
            f"{stages}\n"
            "\n"
            "Function dictionary:\n"
            f"{functions}\n"
            "\n"
            "Original user message:\n"
            f"{raw_text}"
        )

    @staticmethod
    def _format_unit_line(unit: str, description: str | None) -> str:
        if not description:
            return f"- {unit}"
        return f"- {unit}: {description}"

    @staticmethod
    def build_stage_function_hint() -> str:
        return (
            "Pilot definitions:\n"
            "- stage: process/project stage.\n"
            "- function: functional work block."
        )

    def buildStageFunctionHint(self) -> str:
        """Compatibility alias with UML naming."""
        return self.build_stage_function_hint()
