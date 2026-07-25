from state.negotiation_state import NegotiationState

from models.evidence import (
    EvidenceStatus,
)


class EvidenceManager:
    """
    Resolves requested evidence using the patient's
    available laboratory data.
    """

    def resolve(
        self,
        state: NegotiationState,
    ) -> NegotiationState:

        new_state = state.model_copy(
            deep=True,
        )

        patient_labs = (
            new_state.patient_context.patient.labs
        )

        for record in new_state.evidence_ledger:

            if record.status != EvidenceStatus.REQUESTED:
                continue

            lab = patient_labs.get(
                record.lab_name
            )

            if lab is None:
                continue

            record.status = (
                EvidenceStatus.RECEIVED
            )

            record.result = lab

        return new_state