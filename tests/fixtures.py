from datetime import date

from agents.specialists.mock_specialist_runner import MockSpecialistRunner

from models.consensus import ConsensusState
from models.criterion import Criterion
from models.evidence import (
    EvidenceRecord,
    EvidenceStatus,
)
from models.patient import (
    Diagnosis,
    LabResult,
    Medication,
    Patient,
    Sex,
)
from models.patient_context import (
    PatientContext,
    SpecialistType,
)
from models.specialist_output import (
    GuidelineStrength,
    Recommendation,
    SpecialistOutput,
)
from state.negotiation_state import NegotiationState


# -------------------------------------------------
# Mock reasoning rule
# -------------------------------------------------

def nephrology_rule(
    output: SpecialistOutput,
    patient_context: PatientContext,
):
    egfr = patient_context.patient.labs.get("eGFR")

    if egfr is None:
        return

    for recommendation in output.recommendations:

        if recommendation.drug_name.lower() == "metformin":

            recommendation.contraindicated = (
                egfr.value < 30
            )


# -------------------------------------------------
# Base Specialist Output
# -------------------------------------------------

base_output = SpecialistOutput(
    specialist=SpecialistType.NEPHROLOGY,
    confidence=0.95,
    recommendations=[
        Recommendation(
            drug_name="Metformin",
            contraindicated=False,
            clinical_reason="Temporary recommendation",
            guideline_source="KDIGO 2024",
            guideline_strength=GuidelineStrength.STRONG,
            depends_on_evidence=["eGFR"],
        )
    ],
)

cardiology_output = SpecialistOutput(
    specialist=SpecialistType.CARDIOLOGY,
    confidence=0.90,
    recommendations=[
        Recommendation(
            drug_name="Metformin",
            contraindicated=False,
            clinical_reason="No cardiac contraindication.",
            guideline_source="ACC/AHA",
            guideline_strength=GuidelineStrength.MODERATE,
            depends_on_evidence=[],
        )
    ],
)
# -------------------------------------------------
# Mock Runner
# -------------------------------------------------

runner = MockSpecialistRunner(
    cached_outputs={
    SpecialistType.NEPHROLOGY: base_output,
    SpecialistType.CARDIOLOGY: cardiology_output,
},
    rules={
        SpecialistType.NEPHROLOGY: nephrology_rule,
    },
)


# -------------------------------------------------
# Patient
# -------------------------------------------------

patient = Patient(
    patient_id="P001",
    age=68,
    sex=Sex.MALE,
    diagnoses=[
        Diagnosis(name="CKD"),
    ],
    medications=[
        Medication(
            name="Metformin",
            dose="500 mg",
            frequency="BD",
        )
    ],
    labs={
        "eGFR": LabResult(
            value=28,
            unit="mL/min/1.73m²",
            recorded_at=date.today(),
        )
    },
)


# -------------------------------------------------
# Patient Context
# -------------------------------------------------

patient_context = PatientContext(
    patient=patient,
    clinical_summary="CKD patient.",
    active_specialists=[
    SpecialistType.CARDIOLOGY,
    SpecialistType.NEPHROLOGY,
],
    primary_conditions=[],
    key_risks=[],
    missing_information=[],
)


# -------------------------------------------------
# Negotiation State
# -------------------------------------------------

state = NegotiationState(
    iteration=0,
    patient_context=patient_context,
    active_specialists=[
        SpecialistType.NEPHROLOGY,
    ],
    specialist_outputs={
    SpecialistType.CARDIOLOGY: cardiology_output,
    SpecialistType.NEPHROLOGY: base_output,
},
    unresolved_criteria=[
        Criterion(
            drug_name="Metformin",
            conflicting_specialists=[
    SpecialistType.CARDIOLOGY,
    SpecialistType.NEPHROLOGY,
],
            depends_on_evidence=[
                "eGFR",
            ],
        )
    ],
    evidence_ledger=[
        EvidenceRecord(
            lab_name="eGFR",
            status=EvidenceStatus.RECEIVED,
            requested_reason="Need renal function",
            requested_at_iteration=0,
            result=patient.labs["eGFR"],
        )
    ],
    consensus_state=ConsensusState(),
    planner_history=[],
)