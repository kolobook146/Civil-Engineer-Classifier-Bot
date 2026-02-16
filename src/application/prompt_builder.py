from __future__ import annotations

from infrastructure.dictionary_repository import ClassificationDictionary


class PromptBuilder:
    """Builds a pilot classification prompt for Gemini."""

    def build(self, *, raw_text: str, dictionary: ClassificationDictionary) -> str:
        work_types = "\n".join(f"- {item}" for item in dictionary.work_types)
        stages = "\n".join(f"- {item}" for item in dictionary.stages)
        functions = "\n".join(f"- {item}" for item in dictionary.functions)

        return (
            "Ты классификатор фактов выполнения строительного проекта.\n"
            "Верни только JSON без markdown и без пояснений.\n"
            "Поля JSON: volume, unit, workType, stage, function, comment.\n"
            "Для полей workType, stage, function допускается только одно значение из справочника или null.\n"
            "Если поле отсутствует в сообщении, возвращай null.\n"
            f"{self.build_stage_function_hint()}\n"
            "\n"
            "Справочник видов работ:\n"
            f"{work_types}\n"
            "\n"
            "Справочник стадий:\n"
            f"{stages}\n"
            "\n"
            "Справочник функций:\n"
            f"{functions}\n"
            "\n"
            "Исходное сообщение пользователя:\n"
            f"{raw_text}"
        )

    @staticmethod
    def build_stage_function_hint() -> str:
        return (
            "Определения для пилота:\n"
            "- stage: стадия процесса/проекта.\n"
            "- function: функциональный блок работ."
        )

    def buildStageFunctionHint(self) -> str:
        """Compatibility alias with UML naming."""
        return self.build_stage_function_hint()
