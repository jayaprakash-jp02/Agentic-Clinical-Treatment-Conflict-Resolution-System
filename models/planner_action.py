from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, model_validator

from models.patient_context import SpecialistType


class ActionType(str, Enum):
    REQUEST_EVIDENCE = "REQUEST_EVIDENCE"
    RELEASE_SPECIALIST = "RELEASE_SPECIALIST"
    RETAIN = "RETAIN"
    FINALIZE = "FINALIZE"


class PlannerAction(BaseModel):
    action: ActionType

    reason: str

    target_specialist: Optional[SpecialistType] = None

    requested_evidence: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_action(self):
        if self.action in (
            ActionType.RELEASE_SPECIALIST,
            ActionType.RETAIN,
        ):
            if self.target_specialist is None:
                raise ValueError(
                    f"{self.action.value} requires target_specialist."
                )

        if self.action == ActionType.REQUEST_EVIDENCE:
            if not self.requested_evidence:
                raise ValueError(
                    "REQUEST_EVIDENCE requires at least one evidence item."
                )

        if self.action == ActionType.FINALIZE:
            if (
                self.target_specialist is not None
                or self.requested_evidence
            ):
                raise ValueError(
                    "FINALIZE cannot contain specialist or evidence."
                )

        return self