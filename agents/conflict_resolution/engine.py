from agents.conflict_resolution.conflict_detector import detect_conflicts

from models.criterion import Criterion
from models.patient_context import SpecialistType
from models.specialist_output import SpecialistOutput


class ConflictResolutionEngine:
    """
    Converts specialist conflicts into Criterion objects.

    This module DOES NOT:
    - resolve conflicts
    - choose the correct recommendation
    - request evidence
    - call the LLM

    It only identifies what must be resolved.
    """

    def build_criteria(
        self,
        specialist_outputs: dict[SpecialistType, SpecialistOutput],
    ) -> list[Criterion]:

        conflicts = detect_conflicts(specialist_outputs)

        criteria = []

        for drug_name, entries in conflicts.items():

            # Collect unique specialists
            specialists = sorted(
                {specialist for specialist, _ in entries},
                key=lambda s: s.value,
            )

            # Collect all required evidence
            evidence = []

            for _, recommendation in entries:

                evidence.extend(
                    recommendation.depends_on_evidence
                )

            criterion = Criterion(

                drug_name=drug_name,

                conflicting_specialists=specialists,

                depends_on_evidence=sorted(
                    set(evidence)
                ),

            )

            criteria.append(criterion)

        return criteria