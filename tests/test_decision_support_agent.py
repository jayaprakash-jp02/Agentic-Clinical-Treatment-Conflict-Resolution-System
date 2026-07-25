from agents.decision_support.decision_support_agent import (
    DecisionSupportAgent,
)

from agents.planner.consensus_builder import (
    ConsensusBuilder,
)

from agents.planner.evidence_replanner import (
    EvidenceReplanner,
)

from tests.fixtures import (
    runner,
    state,
)

# ----------------------------------------
# Step 1
# Re-run specialists using received evidence
# ----------------------------------------

replanner = EvidenceReplanner(
    runner
)

state = replanner.replan(
    state
)

# ----------------------------------------
# Step 2
# Build consensus
# ----------------------------------------

builder = ConsensusBuilder()

state = builder.build(
    state
)

# ----------------------------------------
# Step 3
# Generate final report
# ----------------------------------------

agent = DecisionSupportAgent()

report = agent.generate_report(
    state
)

print(report)

print()

print("SUCCESS")