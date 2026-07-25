from models.consensus import (
    ConsensusEntry,
    ConsensusState,
    DrugStatus,
)
from models.patient_context import SpecialistType

entry = ConsensusEntry(
    drug_name="Empagliflozin",
    status=DrugStatus.INCLUDED,
    reason="Consensus reached after evidence review.",
    supporting_specialists=[
        SpecialistType.ENDOCRINOLOGY,
        SpecialistType.NEPHROLOGY,
    ],
    conflicting_specialists=[],
    guideline_sources=[
        "ADA 2025",
        "KDIGO 2024",
    ],
)

state = ConsensusState(
    entries=[entry]
)

print(state.model_dump())