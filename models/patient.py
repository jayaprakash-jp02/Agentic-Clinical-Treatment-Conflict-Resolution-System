from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Sex(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"


class Diagnosis(BaseModel):
    name: str
    stage: Optional[str] = None


class Medication(BaseModel):
    name: str
    dose: str
    frequency: str


class LabResult(BaseModel):
    value: float
    unit: str
    recorded_at: date


class BloodPressure(BaseModel):
    systolic: int = Field(gt=0)
    diastolic: int = Field(gt=0)


class VitalSigns(BaseModel):
    weight_kg: Optional[float] = Field(default=None, gt=0)
    blood_pressure: Optional[BloodPressure] = None


class Patient(BaseModel):
    patient_id: str
    age: int = Field(gt=0)
    sex: Sex

    diagnoses: list[Diagnosis]
    medications: list[Medication]
    labs: dict[str, LabResult]

    allergies: list[str] = Field(default_factory=list)
    history: list[str] = Field(default_factory=list)
    symptoms: list[str] = Field(default_factory=list)

    vitals: Optional[VitalSigns] = None