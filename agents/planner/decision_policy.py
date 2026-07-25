from agents.planner.release_rule import find_removable_specialist

from models.evidence import EvidenceStatus
from models.planner_action import (
    ActionType,
    PlannerAction,
)
from state.negotiation_state import NegotiationState


class DecisionPolicy:
    """
    Determines the next planner action.

    Decision Order
    --------------
    1. FINALIZE
    2. REQUEST_EVIDENCE
    3. RELEASE_SPECIALIST
    4. RETAIN

    This class NEVER modifies NegotiationState.
    """

    def decide(
        self,
        state: NegotiationState,
    ) -> PlannerAction:

        # --------------------------------------------------
        # Rule 1
        # No unresolved criteria remain
        # --------------------------------------------------

        if not state.unresolved_criteria:

            return PlannerAction(
                action=ActionType.FINALIZE,
                reason="No unresolved clinical conflicts remain.",
            )

        # --------------------------------------------------
        # Rule 2
        # Check whether required evidence is available
        # --------------------------------------------------

        available_evidence = {
            record.lab_name.lower()
            for record in state.evidence_ledger
            if record.status == EvidenceStatus.RECEIVED
        }

        missing = {
            evidence
            for criterion in state.unresolved_criteria
            for evidence in criterion.depends_on_evidence
            if evidence.lower() not in available_evidence
        }

        if missing:

            return PlannerAction(
                action=ActionType.REQUEST_EVIDENCE,
                reason=(
                    "Additional clinical evidence is required "
                    "before negotiation can continue."
                ),
                requested_evidence=sorted(missing),
            )

        # --------------------------------------------------
        # Rule 3
        # Can a specialist be released?
        # --------------------------------------------------

        removable = find_removable_specialist(state)

        if removable is not None:

            return PlannerAction(
                action=ActionType.RELEASE_SPECIALIST,
                reason=(
                    f"{removable.value} no longer contributes a "
                    "unique clinical position."
                ),
                target_specialist=removable,
            )

        # --------------------------------------------------
        # Rule 4
        # Continue negotiation
        # --------------------------------------------------

        representative = state.active_specialists[0]

        return PlannerAction(
            action=ActionType.RETAIN,
            reason=(
                "All remaining specialists provide unique "
                "clinical positions. Continue negotiation."
            ),
            target_specialist=representative,
        )