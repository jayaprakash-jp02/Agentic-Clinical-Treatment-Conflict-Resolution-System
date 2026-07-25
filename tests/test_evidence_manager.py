from datetime import date

from agents.evidence.evidence_manager import EvidenceManager

from models.consensus import ConsensusState
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
from state.negotiation_state import NegotiationState


patient = Patient(
    patient_id="P001",
    age=68,
    sex=Sex.MALE,
    diagnoses=[
        Diagnosis(
            name="Type 2 Diabetes",
            stage="Type 2",
        )
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

patient_context = PatientContext(
    patient=patient,
    clinical_summary="CKD Patient",
    active_specialists=[
        SpecialistType.NEPHROLOGY,
    ],
    primary_conditions=[
        "CKD",
    ],
    key_risks=[],
    missing_information=[],
)

state = NegotiationState(
    iteration=0,
    patient_context=patient_context,
    active_specialists=[
        SpecialistType.NEPHROLOGY,
    ],
    specialist_outputs={},
    unresolved_criteria=[],
    evidence_ledger=[
        EvidenceRecord(
            lab_name="eGFR",
            status=EvidenceStatus.REQUESTED,
            requested_reason="Need renal function.",
            requested_at_iteration=0,
        )
    ],
    consensus_state=ConsensusState(),
    planner_history=[],
)

manager = EvidenceManager()

new_state = manager.resolve(state)

print("=" * 70)
print("Evidence Manager Test")
print("=" * 70)

record = new_state.evidence_ledger[0]

print()

print("Lab Name :", record.lab_name)

print("Status   :", record.status)

print("Result   :", record.result)

print()

assert record.status == EvidenceStatus.RECEIVED

assert record.result is not None

print("SUCCESS")