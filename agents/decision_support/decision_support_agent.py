from state.negotiation_state import NegotiationState


class DecisionSupportAgent:
    """
    Converts the ConsensusState into a
    human-readable clinical recommendation.

    This module NEVER performs reasoning.

    It only explains the final consensus.
    """

    def generate_report(
        self,
        state: NegotiationState,
    ) -> str:

        report = []

        report.append("=" * 70)
        report.append("FINAL CLINICAL RECOMMENDATION")
        report.append("=" * 70)
        report.append("")

        if not state.consensus_state.entries:

            report.append(
                "No consensus recommendations available."
            )

            return "\n".join(report)

        for entry in state.consensus_state.entries:

            report.append(
                f"Drug : {entry.drug_name}"
            )

            report.append(
                f"Decision : {entry.status.value}"
            )

            report.append(
                f"Reason : {entry.reason}"
            )

            report.append(
                "Supporting Specialists : "
                + ", ".join(
                    specialist.value
                    for specialist
                    in entry.supporting_specialists
                )
            )

            if entry.conflicting_specialists:

                report.append(
                    "Opposing Specialists : "
                    + ", ".join(
                        specialist.value
                        for specialist
                        in entry.conflicting_specialists
                    )
                )

            if entry.guideline_sources:

                report.append(
                    "Guidelines : "
                    + ", ".join(
                        entry.guideline_sources
                    )
                )

            report.append("")

        return "\n".join(report)