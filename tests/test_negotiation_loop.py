from agents.planner.consensus_builder import (
    ConsensusBuilder,
)
from agents.planner.evidence_replanner import (
    EvidenceReplanner,
)
from agents.planner.negotiation_loop import (
    NegotiationLoop,
)
from agents.planner.planner import Planner

from tests.fixtures import (
    runner,
    state,
)

planner = Planner()

replanner = EvidenceReplanner(
    runner
)

builder = ConsensusBuilder()

loop = NegotiationLoop(

    planner=planner,

    replanner=replanner,

    consensus_builder=builder,

)

final_state = loop.run(
    state
)

print("=" * 70)
print("Negotiation Loop Test")
print("=" * 70)

print()

print(
    "Remaining Criteria:",
    len(
        final_state.unresolved_criteria
    ),
)

print()

print(
    "Consensus Entries:",
    len(
        final_state.consensus_state.entries
    ),
)

print()

print(
    "Planner History:",
    len(
        final_state.planner_history
    ),
)

print()

print("SUCCESS")