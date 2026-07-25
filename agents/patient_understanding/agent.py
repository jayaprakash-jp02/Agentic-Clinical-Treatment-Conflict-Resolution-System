import json

from pydantic import ValidationError

from config import MAX_ATTEMPTS
from models.patient import Patient
from models.patient_context import (
    PatientContext,
    SpecialistType,
)

from .llm_client import call_model
from .parser import parse_response
from .prompt_builder import build_prompt
from .validator import validate_output


def run_patient_understanding(patient: Patient) -> PatientContext:
    prompt = build_prompt(patient)

    last_error = None

    for attempt in range(MAX_ATTEMPTS):
        try:
            raw_response = call_model(prompt)

            parsed_response = parse_response(raw_response)

            validated_output = validate_output(parsed_response)

            break

        except (
            json.JSONDecodeError,
            ValidationError,
            ValueError,
        ) as error:
            last_error = error

            if attempt == MAX_ATTEMPTS - 1:
                raise RuntimeError(
                    f"Patient Understanding Agent failed after "
                    f"{MAX_ATTEMPTS} attempts."
                ) from error

    specialists = []

    for specialist_name in validated_output.active_specialists:
        try:
            specialists.append(
                SpecialistType(specialist_name)
            )
        except ValueError as error:
            raise RuntimeError(
                f"Unsupported specialist returned: "
                f"{specialist_name}"
            ) from error

    if not specialists:
        raise RuntimeError(
            "No specialist selected by Patient Understanding Agent."
        )

    return PatientContext(
        patient=patient,
        clinical_summary=validated_output.clinical_summary,
        active_specialists=specialists,
        primary_conditions=validated_output.primary_conditions,
        key_risks=validated_output.key_risks,
        missing_information=validated_output.missing_information,
    )