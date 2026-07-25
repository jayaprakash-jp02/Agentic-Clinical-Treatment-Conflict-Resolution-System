from agents.conflict_resolution.engine import (
    ConflictResolutionEngine,
)
from agents.decision_support.decision_support_agent import (
    DecisionSupportAgent,
)
from agents.planner.consensus_builder import (
    ConsensusBuilder,
)
from agents.planner.evidence_replanner import (
    EvidenceReplanner,
)
from agents.planner.negotiation_loop import (
    NegotiationLoop,
)
from agents.planner.planner import (
    Planner,
)
from agents.specialists.specialist_runner import (
    SpecialistRunner,
)


class ClinicalPipeline:
    """
    High-level application orchestrator.

    Coordinates the complete workflow.

    It NEVER performs reasoning itself.
    """

    def __init__(
        self,
        specialist_runner: SpecialistRunner,
    ):

        self.runner = specialist_runner

        self.conflict_engine = (
            ConflictResolutionEngine()
        )

        self.planner = Planner()

        self.replanner = (
            EvidenceReplanner(
                specialist_runner
            )
        )

        self.consensus_builder = (
            ConsensusBuilder()
        )

        self.negotiation_loop = (
            NegotiationLoop(
                planner=self.planner,
                replanner=self.replanner,
                consensus_builder=self.consensus_builder,
            )
        )

        self.decision_support = (
            DecisionSupportAgent()
        )