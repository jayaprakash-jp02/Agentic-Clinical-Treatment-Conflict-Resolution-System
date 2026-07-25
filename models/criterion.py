from pydantic import BaseModel, Field

from models.patient_context import SpecialistType


class Criterion(BaseModel):
    drug_name: str

    conflicting_specialists: list[SpecialistType] = Field(min_length=2)

    depends_on_evidence: list[str] = Field(default_factory=list)