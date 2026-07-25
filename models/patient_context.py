from enum import Enum

from pydantic import BaseModel, Field

from models.patient import Patient


class SpecialistType(str, Enum):
    CARDIOLOGY = "Cardiology"
    NEPHROLOGY = "Nephrology"
    ENDOCRINOLOGY = "Endocrinology"


class PatientContext(BaseModel):
    patient: Patient

    clinical_summary: str

    active_specialists: list[SpecialistType] = Field(min_length=1)

    primary_conditions: list[str] = Field(default_factory=list)

    key_risks: list[str] = Field(default_factory=list)

    missing_information: list[str] = Field(default_factory=list)