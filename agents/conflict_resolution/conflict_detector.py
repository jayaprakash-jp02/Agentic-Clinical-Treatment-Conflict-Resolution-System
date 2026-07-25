from collections import defaultdict

from models.patient_context import SpecialistType
from models.specialist_output import Recommendation

def detect_conflicts(
    specialist_outputs: dict,
) -> dict[str, list[tuple[SpecialistType, Recommendation]]]:
    """
    Detect recommendations that disagree.

    Returns:

    {
        "metformin": [
            Recommendation(...),
            Recommendation(...)
        ]
    }
    """

    grouped = defaultdict(list)

    for output in specialist_outputs.values():

        for recommendation in output.recommendations:

                    grouped[
            recommendation.drug_name.lower()
        ].append(
            (
                output.specialist,
                recommendation,
            )
        )

    conflicts = {}

    for drug, recommendations in grouped.items():

        decisions = {
            recommendation.contraindicated
            for _, recommendation in recommendations
        }

        if len(decisions) > 1:

            conflicts[drug] = recommendations

    return conflicts