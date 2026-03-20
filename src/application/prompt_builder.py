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
            "For workType, only one dictionary value or null is allowed.\n"
            "For stage and function:\n"
            "- MUST return exactly one value from the corresponding dictionary.\n"
            "- NEVER return null for stage or function.\n"
            "- If explicit evidence is weak or missing, infer the closest semantic match from the message.\n"
            "- If multiple options are close, choose the most probable one and put ambiguity notes into comment.\n"
            "If a field is missing in the message, return null, except stage and function which must still be selected.\n"
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
            "- function = functional workstream (what is being delivered/managed).\n"
            "- stage = lifecycle gate within a function (where this workstream is now)."
        )

    def buildStageFunctionHint(self) -> str:
        """Compatibility alias with UML naming."""
        return self.build_stage_function_hint()
