from datetime import date

from prompts.specialist_prompt_builder import SpecialistPromptBuilder

from models.patient import (
    BloodPressure,
    Diagnosis,
    LabResult,
    Medication,
    Patient,
    Sex,
    VitalSigns,
)
from models.patient_context import (
    PatientContext,
    SpecialistType,
)


def main():

    patient = Patient(
        patient_id="P001",
        age=65,
        sex=Sex.MALE,
        diagnoses=[
            Diagnosis(name="Type 2 Diabetes"),
            Diagnosis(name="CKD", stage="Stage 4"),
        ],
        medications=[
            Medication(
                name="Metformin",
                dose="500 mg",
                frequency="Twice Daily",
            )
        ],
        labs={
            "eGFR": LabResult(
                value=28,
                unit="mL/min/1.73m²",
                recorded_at=date.today(),
            )
        },
        vitals=VitalSigns(
            weight_kg=78,
            blood_pressure=BloodPressure(
                systolic=150,
                diastolic=92,
            ),
        ),
    )

    patient_context = PatientContext(
        patient=patient,
        clinical_summary="Type 2 Diabetes with Stage 4 CKD.",
        active_specialists=[
            SpecialistType.NEPHROLOGY,
        ],
        primary_conditions=[
            "Type 2 Diabetes",
            "CKD",
        ],
        key_risks=[
            "eGFR = 28",
        ],
        missing_information=[],
    )

    builder = SpecialistPromptBuilder()

    prompt = builder.build_prompt(
        specialist=SpecialistType.NEPHROLOGY,
        patient_context=patient_context,
        retrieved_chunks=[
            {
                "guideline": "KDIGO_2024",
                "text": "Metformin should not be used when eGFR is below 30."
            }
        ],
    )

    print(prompt)


if __name__ == "__main__":
    main()