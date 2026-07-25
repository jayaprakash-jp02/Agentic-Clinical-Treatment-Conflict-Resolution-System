from datetime import date

from agents.planner.decision_policy import DecisionPolicy

from models.consensus import ConsensusState
from models.criterion import Criterion
from models.evidence import EvidenceRecord, EvidenceStatus
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
)

# ==========================================================
# Context
# ==========================================================

context = PatientContext(
    patient=patient,
    clinical_summary="CKD + Diabetes",
    active_specialists=[
        SpecialistType.CARDIOLOGY,
        SpecialistType.NEPHROLOGY,
    ],
    primary_conditions=[
        "CKD",
        "Diabetes",
    ],
    key_risks=[],
    missing_information=[],
)

# ==========================================================
# Specialist Outputs
# ==========================================================

cardiology = SpecialistOutput(
    specialist=SpecialistType.CARDIOLOGY,
    confidence=0.9,
    recommendations=[
        Recommendation(
            drug_name="Metformin",
            contraindicated=False,
            clinical_reason="Safe",
            guideline_source="ACC/AHA",
            guideline_strength=GuidelineStrength.MODERATE,
        )
    ],
)

nephrology = SpecialistOutput(
    specialist=SpecialistType.NEPHROLOGY,
    confidence=0.95,
    recommendations=[
        Recommendation(
            drug_name="Metformin",
            contraindicated=True,
            clinical_reason="Low eGFR",
            guideline_source="KDIGO",
            guideline_strength=GuidelineStrength.STRONG,
            depends_on_evidence=["eGFR"],
        )
    ],
)

# ==========================================================
# Criterion
# ==========================================================

criterion = Criterion(
    drug_name="Metformin",
    conflicting_specialists=[
        SpecialistType.CARDIOLOGY,
        SpecialistType.NEPHROLOGY,
    ],
    depends_on_evidence=[
        "eGFR",
    ],
)

# ==========================================================
# Negotiation State
# ==========================================================

state = NegotiationState(
    iteration=0,
    patient_context=context,
    active_specialists=[
        SpecialistType.CARDIOLOGY,
        SpecialistType.NEPHROLOGY,
    ],
    specialist_outputs={
        SpecialistType.CARDIOLOGY: cardiology,
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
# Planner
# ==========================================================

policy = DecisionPolicy()

action = policy.decide(state)

print("=" * 70)
print("Decision Policy Test")
print("=" * 70)

print(action.model_dump())