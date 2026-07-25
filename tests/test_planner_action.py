from models.patient_context import SpecialistType
from models.planner_action import (
    ActionType,
    PlannerAction,
)

release_action = PlannerAction(
    action=ActionType.RELEASE_SPECIALIST,
    reason="Removing Nephrology does not change the consensus treatment set.",
    target_specialist=SpecialistType.NEPHROLOGY,
)

evidence_action = PlannerAction(
    action=ActionType.REQUEST_EVIDENCE,
    reason="Updated eGFR could change Metformin eligibility.",
    requested_evidence=["eGFR"],
)

finalize_action = PlannerAction(
    action=ActionType.FINALIZE,
    reason="No remaining action can change the treatment decision.",
)

print(release_action.model_dump())
print(evidence_action.model_dump())
print(finalize_action.model_dump())