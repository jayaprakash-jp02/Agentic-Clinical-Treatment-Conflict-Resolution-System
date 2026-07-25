from datetime import date

from agents.specialists.real_specialist_runner import RealSpecialistRunner
from knowledge.retriever import GuidelineRetriever
from llm.ollama_client import OllamaClient

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

from prompts.specialist_prompt_builder import SpecialistPromptBuilder


def build_patient_context():

    patient = Patient(
        patient_id="P001",
        age=65,
        sex=Sex.MALE,
        diagnoses=[
            Diagnosis(
                name="Type 2 Diabetes",
            ),
            Diagnosis(
                name="CKD",
                stage="Stage 4",
            ),
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

    return PatientContext(
        patient=patient,
        clinical_summary="Type 2 Diabetes with Stage 4 CKD.",
        active_specialists=[
            SpecialistType.NEPHROLOGY,
        ],
        primary_conditions=[
            "Type 2 Diabetes",
            "CKD Stage 4",
        ],
        key_risks=[
            "eGFR = 28",
        ],
        missing_information=[],
    )


def main():

    retriever = GuidelineRetriever()

    prompt_builder = SpecialistPromptBuilder()

    llm = OllamaClient(
        model="qwen2.5:7b",
    )

    runner = RealSpecialistRunner(
        retriever=retriever,
        prompt_builder=prompt_builder,
        llm=llm,
    )

    output = runner.run(
        specialist=SpecialistType.NEPHROLOGY,
        patient_context=build_patient_context(),
    )

    print("\n==============================")
    print("SPECIALIST OUTPUT")
    print("==============================\n")

    print(
        output.model_dump_json(
            indent=2,
        )
    )


if __name__ == "__main__":
    main()