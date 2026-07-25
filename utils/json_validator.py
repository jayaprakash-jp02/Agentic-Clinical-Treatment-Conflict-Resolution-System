import json
import re

from models.specialist_output import SpecialistOutput


class JSONValidator:
    """
    Cleans, parses and validates LLM JSON responses.
    """

    @staticmethod
    def _extract_json(text: str) -> str:
        """
        Extract JSON even if the model wraps it in
        markdown or explanatory text.
        """

        text = text.strip()

        # Remove ```json ... ```
        text = re.sub(r"^```json", "", text, flags=re.IGNORECASE)
        text = re.sub(r"^```", "", text)
        text = re.sub(r"```$", "", text)

        text = text.strip()

        # Find first JSON object
        start = text.find("{")
        end = text.rfind("}")

        if start == -1 or end == -1:
            raise ValueError("No JSON object found.")

        return text[start:end + 1]

    @classmethod
    def validate(
        cls,
        raw_response: str,
    ) -> SpecialistOutput:
        """
        Convert raw LLM output into SpecialistOutput.
        """

        cleaned = cls._extract_json(raw_response)

        try:
            data = json.loads(cleaned)

        except json.JSONDecodeError as e:
            raise ValueError(
                f"Invalid JSON returned by LLM:\n\n{cleaned}"
            ) from e

        return SpecialistOutput.model_validate(data)