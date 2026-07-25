from enum import Enum

from pydantic import BaseModel, Field

from models.patient_context import SpecialistType


class DrugStatus(str, Enum):
    INCLUDED = "Included"
    EXCLUDED = "Excluded"


class ConsensusEntry(BaseModel):
    drug_name: str

    status: DrugStatus

    reason: str

    supporting_specialists: list[SpecialistType] = Field(default_factory=list)

    conflicting_specialists: list[SpecialistType] = Field(default_factory=list)

    guideline_sources: list[str] = Field(default_factory=list)


class ConsensusState(BaseModel):
    entries: list[ConsensusEntry] = Field(default_factory=list)