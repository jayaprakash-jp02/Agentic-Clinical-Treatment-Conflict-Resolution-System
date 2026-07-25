from datetime import date

from agents.planner.release_rule import find_removable_specialist

from models.consensus import ConsensusState
from models.criterion import Criterion
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


# ==========================================================
# Patient
# ==========================================================

patient = Patient(
    patient_id="P001",
    age=68,
    sex=Sex.MALE,
    diagnoses=[
        Diagnosis(
            name="Type 2 Diabetes",
            stage="Type 2",
        ),
        Diagnosis(
            name="Chronic Kidney Disease",
            stage="Stage 3b",
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
            recorded_at=date(2026, 4, 1),
        )
    },
    history=["Hypertension"],
    symptoms=["Fatigue"],
)

# ==========================================================
# Patient Context
# ==========================================================

patient_context = PatientContext(
    patient=patient,
    clinical_summary="CKD + Diabetes patient",
    active_specialists=[
        SpecialistType.CARDIOLOGY,
        SpecialistType.ENDOCRINOLOGY,
        SpecialistType.NEPHROLOGY,
    ],
    primary_conditions=[
        "Type 2 Diabetes",
        "Chronic Kidney Disease",
    ],
    key_risks=[
        "Progressive CKD",
    ],
    missing_information=[],
)

# ==========================================================
# Specialist Outputs
# ==========================================================

cardiology = SpecialistOutput(
    specialist=SpecialistType.CARDIOLOGY,
    confidence=0.90,
    recommendations=[
        Recommendation(
            drug_name="Metformin",
            contraindicated=False,
            clinical_reason="Cardiology has no contraindication.",
            guideline_source="ACC/AHA",
            guideline_strength=GuidelineStrength.MODERATE,
        )
    ],
)

endocrinology = SpecialistOutput(
    specialist=SpecialistType.ENDOCRINOLOGY,
    confidence=0.95,
    recommendations=[
        Recommendation(
            drug_name="Metformin",
            contraindicated=False,
            clinical_reason="Good glycemic control.",
            guideline_source="ADA 2025",
            guideline_strength=GuidelineStrength.STRONG,
        )
    ],
)

nephrology = SpecialistOutput(
    specialist=SpecialistType.NEPHROLOGY,
    confidence=0.98,
    recommendations=[
        Recommendation(
            drug_name="Metformin",
            contraindicated=True,
            clinical_reason="eGFR below safe threshold.",
            guideline_source="KDIGO 2024",
            guideline_strength=GuidelineStrength.STRONG,
            depends_on_evidence=["eGFR"],
        )
    ],
)

# ==========================================================
# Conflict Criterion
# ==========================================================

criterion = Criterion(
    drug_name="Metformin",
    conflicting_specialists=[
        SpecialistType.CARDIOLOGY,
        SpecialistType.ENDOCRINOLOGY,
        SpecialistType.NEPHROLOGY,
    ],
    depends_on_evidence=["eGFR"],
)

# ==========================================================
# Negotiation State
# ==========================================================

state = NegotiationState(
    iteration=0,
    patient_context=patient_context,
    active_specialists=[
        SpecialistType.CARDIOLOGY,
        SpecialistType.ENDOCRINOLOGY,
        SpecialistType.NEPHROLOGY,
    ],
    specialist_outputs={
        SpecialistType.CARDIOLOGY: cardiology,
        SpecialistType.ENDOCRINOLOGY: endocrinology,
        SpecialistType.NEPHROLOGY: nephrology,
    },
    unresolved_criteria=[
        criterion,
    ],
    evidence_ledger=[],
    consensus_state=ConsensusState(),
    planner_history=[],
)

# ==========================================================
# Test
# ==========================================================

print("=" * 70)
print("Release Rule Test")
print("=" * 70)

removable = find_removable_specialist(state)

print()

print("Suggested removable specialist:")

print(removable)

print()

assert removable in (
    SpecialistType.CARDIOLOGY,
    SpecialistType.ENDOCRINOLOGY,
)

print("SUCCESS")