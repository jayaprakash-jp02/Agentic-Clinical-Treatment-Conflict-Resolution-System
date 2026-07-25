from pydantic import BaseModel, Field

from models.consensus import ConsensusState
from models.criterion import Criterion
from models.evidence import EvidenceRecord
from models.patient_context import PatientContext, SpecialistType
from models.planner_action import PlannerAction
from models.specialist_output import SpecialistOutput


class NegotiationState(BaseModel):

    iteration: int = 0

    patient_context: PatientContext

    active_specialists: list[SpecialistType] = Field(min_length=1)

    specialist_outputs: dict[SpecialistType, SpecialistOutput] = Field(
        default_factory=dict
    )

    unresolved_criteria: list[Criterion] = Field(default_factory=list)

    evidence_ledger: list[EvidenceRecord] = Field(default_factory=list)

    consensus_state: ConsensusState

    planner_history: list[PlannerAction] = Field(default_factory=list)