from models.consensus import (
    ConsensusEntry,
    ConsensusState,
    DrugStatus,
)
from models.evidence import EvidenceStatus
from state.negotiation_state import NegotiationState


class ConsensusBuilder:
    """
    Builds the final consensus.

    Cases
    -----
    1. No conflicts:
       All specialist recommendations are copied directly
       into the final consensus.

    2. Conflicts:
       Resolve according to the current resolution policy.
    """

    def build(
        self,
        state: NegotiationState,
    ) -> NegotiationState:

        new_state = state.model_copy(deep=True)

        # ==========================================================
        # CASE 1 : NO CONFLICTS
        # ==========================================================

        if not new_state.unresolved_criteria:

            if new_state.consensus_state.entries:
                return new_state

            added = set()

            for specialist, output in new_state.specialist_outputs.items():

                for recommendation in output.recommendations:

                    key = recommendation.drug_name.lower()

                    if key in added:
                        continue

                    added.add(key)

                    status = (
                        DrugStatus.EXCLUDED
                        if recommendation.contraindicated
                        else DrugStatus.INCLUDED
                    )

                    reason = recommendation.clinical_reason

                    new_state.consensus_state.entries.append(

                        ConsensusEntry(
                            drug_name=recommendation.drug_name,
                            status=status,
                            reason=reason,
                            supporting_specialists=[specialist],
                            conflicting_specialists=[],
                            guideline_sources=[
                                recommendation.guideline_source
                            ],
                        )

                    )

            return new_state

        # ==========================================================
        # CASE 2 : CONFLICT RESOLUTION
        # ==========================================================

        received_evidence = {

            record.lab_name.lower()

            for record in new_state.evidence_ledger

            if record.status == EvidenceStatus.RECEIVED

        }

        resolved = []

        for criterion in new_state.unresolved_criteria:

            evidence_complete = all(

                item.lower() in received_evidence

                for item in criterion.depends_on_evidence

            )

            if not evidence_complete:
                continue

            contraindicated = False

            supporting = []

            conflicting = []

            guideline_sources = []

            for specialist in criterion.conflicting_specialists:

                output = new_state.specialist_outputs.get(
                    specialist
                )

                if output is None:
                    continue

                for recommendation in output.recommendations:

                    if (
                        recommendation.drug_name.lower()
                        != criterion.drug_name.lower()
                    ):
                        continue

                    guideline_sources.append(
                        recommendation.guideline_source
                    )

                    if recommendation.contraindicated:

                        contraindicated = True
                        supporting.append(specialist)

                    else:

                        conflicting.append(specialist)

            status = (
                DrugStatus.EXCLUDED
                if contraindicated
                else DrugStatus.INCLUDED
            )

            reason = (
                "Drug excluded because at least one specialist still considers it contraindicated after evidence review."
                if contraindicated
                else "All specialists consider the drug appropriate after evidence review."
            )

            new_state.consensus_state.entries.append(

                ConsensusEntry(
                    drug_name=criterion.drug_name,
                    status=status,
                    reason=reason,
                    supporting_specialists=supporting,
                    conflicting_specialists=conflicting,
                    guideline_sources=sorted(
                        set(guideline_sources)
                    ),
                )

            )

            resolved.append(criterion)

        new_state.unresolved_criteria = [

            criterion

            for criterion in new_state.unresolved_criteria

            if criterion not in resolved

        ]

        return new_state