from agents.planner.decision_policy import DecisionPolicy

from models.evidence import (
    EvidenceRecord,
    EvidenceStatus,
)
from models.planner_action import (
    ActionType,
    PlannerAction,
)

from state.negotiation_state import NegotiationState


class Planner:
    """
    Executes exactly ONE planner step.

    Responsibilities
    ----------------
    - Ask the DecisionPolicy for the next action.
    - Apply that action.
    - Return a NEW NegotiationState.

    This class contains NO clinical reasoning.
    """

    def __init__(self):

        self.policy = DecisionPolicy()

    def step(
        self,
        state: NegotiationState,
    ) -> NegotiationState:

        action = self.policy.decide(state)

        if action.action == ActionType.REQUEST_EVIDENCE:

            return self._request_evidence(
                state,
                action,
            )

        if action.action == ActionType.RELEASE_SPECIALIST:

            return self._release_specialist(
                state,
                action,
            )

        if action.action == ActionType.RETAIN:

            return self._retain(
                state,
                action,
            )

        return self._finalize(
            state,
            action,
        )

    # ==========================================================
    # REQUEST_EVIDENCE
    # ==========================================================

    def _request_evidence(
        self,
        state: NegotiationState,
        action: PlannerAction,
    ) -> NegotiationState:

        new_state = state.model_copy(
            deep=True,
        )

        for lab in action.requested_evidence:

            already_requested = any(

                record.lab_name.lower() == lab.lower()

                and record.status
                == EvidenceStatus.REQUESTED

                for record in new_state.evidence_ledger

            )

            if already_requested:
                continue

            new_state.evidence_ledger.append(

                EvidenceRecord(

                    lab_name=lab,

                    status=EvidenceStatus.REQUESTED,

                    requested_reason=action.reason,

                    requested_at_iteration=new_state.iteration,

                )

            )

        new_state.planner_history.append(action)

        new_state.iteration += 1

        return new_state

    # ==========================================================
    # RELEASE_SPECIALIST
    # ==========================================================

    def _release_specialist(
        self,
        state: NegotiationState,
        action: PlannerAction,
    ) -> NegotiationState:

        new_state = state.model_copy(
            deep=True,
        )

        new_state.active_specialists = [

            specialist

            for specialist in new_state.active_specialists

            if specialist != action.target_specialist

        ]

        new_state.planner_history.append(action)

        new_state.iteration += 1

        return new_state

    # ==========================================================
    # RETAIN
    # ==========================================================

    def _retain(
        self,
        state: NegotiationState,
        action: PlannerAction,
    ) -> NegotiationState:

        new_state = state.model_copy(
            deep=True,
        )

        new_state.planner_history.append(
            action,
        )

        new_state.iteration += 1

        return new_state

    # ==========================================================
    # FINALIZE
    # ==========================================================

    def _finalize(
        self,
        state: NegotiationState,
        action: PlannerAction,
    ) -> NegotiationState:

        new_state = state.model_copy(
            deep=True,
        )

        new_state.planner_history.append(
            action,
        )

        # FINALIZE is not a negotiation round.
        # Therefore iteration is NOT incremented.

        return new_state