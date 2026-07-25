from enum import Enum

from pydantic import BaseModel, Field

from models.patient_context import SpecialistType


class GuidelineStrength(str, Enum):
    STRONG = "Strong"
    MODERATE = "Moderate"
    WEAK = "Weak"


class Recommendation(BaseModel):
    drug_name: str

    contraindicated: bool = False

    clinical_reason: str

    guideline_source: str

    guideline_strength: GuidelineStrength

    depends_on_evidence: list[str] = Field(default_factory=list)


class SpecialistOutput(BaseModel):
    specialist: SpecialistType

    recommendations: list[Recommendation] = Field(min_length=1)

    confidence: float = Field(ge=0.0, le=1.0)

    missing_evidence: list[str] = Field(default_factory=list)