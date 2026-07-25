from agents.planner.evidence_replanner import (
    EvidenceReplanner,
)

from tests.fixtures import (
    runner,
    state,
)

from models.patient_context import (
    SpecialistType,
)

replanner = EvidenceReplanner(
    runner,
)

new_state = replanner.replan(
    state,
)

print("=" * 70)
print("Evidence Replanner Test")
print("=" * 70)

output = new_state.specialist_outputs[
    SpecialistType.NEPHROLOGY
]

print()

print("Contraindicated:")

print(
    output.recommendations[0].contraindicated
)

print()

print("Remaining Criteria:")

print(
    len(new_state.unresolved_criteria)
)

print()

print("SUCCESS")