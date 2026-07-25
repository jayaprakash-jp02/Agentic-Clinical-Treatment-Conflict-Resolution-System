from state.negotiation_state import NegotiationState

from models.patient_context import SpecialistType


def get_specialist_position(
    specialist: SpecialistType,
    drug_name: str,
    state: NegotiationState,
) -> bool | None:
    """
    Returns

    True  -> contraindicated

    False -> not contraindicated

    None  -> specialist never commented on this drug
    """

    output = state.specialist_outputs.get(
        specialist
    )

    if output is None:
        return None

    for recommendation in output.recommendations:

        if recommendation.drug_name.lower() == drug_name.lower():

            return recommendation.contraindicated

    return None


def has_unique_position(
    specialist: SpecialistType,
    state: NegotiationState,
) -> bool:
    """
    Returns True if this specialist provides
    at least one unique clinical position.
    """

    for criterion in state.unresolved_criteria:

        if specialist not in criterion.conflicting_specialists:
            continue

        position = get_specialist_position(
            specialist,
            criterion.drug_name,
            state,
        )
        if position is None:
            continue
        represented_elsewhere = any(

            other != specialist

            and other in state.active_specialists

            and get_specialist_position(
                other,
                criterion.drug_name,
                state,
            ) is not None

            and get_specialist_position(
                other,
                criterion.drug_name,
                state,
            ) == position

            for other in criterion.conflicting_specialists

    )

        if not represented_elsewhere:

            return True

    return False


def find_removable_specialist(
    state: NegotiationState,
) -> SpecialistType | None:
    """
    Returns one removable specialist.

    Returns None if every active specialist
    is still required.
    """

    for specialist in state.active_specialists:

        if not has_unique_position(
            specialist,
            state,
        ):

            return specialist

    return None