from __future__ import annotations

from infrastructure.dictionary_repository import ClassificationDictionary


class PromptBuilder:
    """Builds a pilot classification prompt for Gemini."""

    def build(self, *, raw_text: str, dictionary: ClassificationDictionary) -> str:
        work_types = "\n".join(f"- {item}" for item in dictionary.work_types)
        stages = "\n".join(f"- {item}" for item in dictionary.stages)
        functions = "\n".join(f"- {item}" for item in dictionary.functions)

        return (
            "You are a classifier of construction project progress facts.\n"
            "Return JSON only, without markdown and without explanations.\n"
            "JSON fields: volume, unit, workType, stage, function, comment.\n"
            "For workType, stage, and function, only one dictionary value or null is allowed.\n"
            "If a field is missing in the message, return null.\n"
            f"{self.build_stage_function_hint()}\n"
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
    def build_stage_function_hint() -> str:
        return (
            "Pilot definitions:\n"
            "- stage: process/project stage.\n"
            "- function: functional work block."
        )

    def buildStageFunctionHint(self) -> str:
        """Compatibility alias with UML naming."""
        return self.build_stage_function_hint()
