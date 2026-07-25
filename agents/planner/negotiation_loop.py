from agents.planner.consensus_builder import (
    ConsensusBuilder,
)
from agents.planner.evidence_replanner import (
    EvidenceReplanner,
)
from agents.planner.planner import Planner
from state.negotiation_state import (
    NegotiationState,
)


class NegotiationLoop:
    """
    Executes the complete negotiation process.

    Responsibilities
    ----------------
    - Run planner
    - Replan specialists after evidence
    - Build consensus
    - Stop when no unresolved criteria remain
    """

    def __init__(
        self,
        planner: Planner,
        replanner: EvidenceReplanner,
        consensus_builder: ConsensusBuilder,
        max_iterations: int = 10,
    ):

        self.planner = planner

        self.replanner = replanner

        self.consensus_builder = (
            consensus_builder
        )

        self.max_iterations = (
            max_iterations
        )

    def run(
        self,
        state: NegotiationState,
    ) -> NegotiationState:

        current_state = state

        if not current_state.unresolved_criteria:
            return self.consensus_builder.build(current_state)

        for _ in range(self.max_iterations):

            if not current_state.unresolved_criteria:
                break

            current_state = self.planner.step(current_state)
            current_state = self.replanner.replan(current_state)
            current_state = self.consensus_builder.build(current_state)

        return current_state