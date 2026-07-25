from agents.specialists.specialist_runner import SpecialistRunner


from agents.conflict_resolution.engine import (
    ConflictResolutionEngine,
)

from models.evidence import EvidenceStatus

from state.negotiation_state import (
    NegotiationState,
)


class EvidenceReplanner:
    """
    Re-runs affected specialists whenever
    new clinical evidence becomes available.

    Responsibilities
    ----------------
    - Detect newly received evidence.
    - Re-run only specialists depending on it.
    - Replace their previous SpecialistOutput.
    - Recompute conflicts.
    """

    def __init__(
    self,
    specialist_runner: SpecialistRunner,
):

     self.runner = specialist_runner

     self.engine = ConflictResolutionEngine()

    def replan(
        self,
        state: NegotiationState,
    ) -> NegotiationState:

        new_state = state.model_copy(
            deep=True,
        )

        available = {

            record.lab_name

            for record in new_state.evidence_ledger

            if record.status == EvidenceStatus.RECEIVED

        }

        for specialist, output in list(
            new_state.specialist_outputs.items()
        ):

            needs_rerun = False

            for recommendation in output.recommendations:

                if any(

                    evidence in available

                    for evidence in recommendation.depends_on_evidence

                ):

                    needs_rerun = True

                    break

            if not needs_rerun:
                continue

            new_output = self.runner.run(
    specialist=specialist,
    patient_context=new_state.patient_context,
)

            new_state.specialist_outputs[
                specialist
            ] = new_output

        new_state.unresolved_criteria = (
            self.engine.build_criteria(
                new_state.specialist_outputs
            )
        )

        return new_state