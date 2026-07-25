from agents.planner.consensus_builder import (
    ConsensusBuilder,
)

from tests.fixtures import (
    state,
)

builder = ConsensusBuilder()

new_state = builder.build(
    state
)

print("=" * 70)
print("Consensus Builder Test")
print("=" * 70)

print()

print(
    "Consensus Entries:",
    len(new_state.consensus_state.entries),
)

print()

for entry in new_state.consensus_state.entries:

    print(entry.model_dump())

print()

print(
    "Remaining Criteria:",
    len(new_state.unresolved_criteria),
)

print()

print("SUCCESS")