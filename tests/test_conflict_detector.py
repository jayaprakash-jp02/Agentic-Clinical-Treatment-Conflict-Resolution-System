from agents.conflict_resolution.conflict_detector import detect_conflicts
from models.patient_context import SpecialistType
from models.specialist_output import (
    GuidelineStrength,
    Recommendation,
    SpecialistOutput,
)


cardiology = SpecialistOutput(
    specialist=SpecialistType.CARDIOLOGY,
    confidence=0.90,
    recommendations=[
        Recommendation(
            drug_name="Metformin",
            contraindicated=False,
            clinical_reason="Cardiology has no contraindication.",
            guideline_source="ACC/AHA",
            guideline_strength=GuidelineStrength.MODERATE,
        )
    ],
)

nephrology = SpecialistOutput(
    specialist=SpecialistType.NEPHROLOGY,
    confidence=0.95,
    recommendations=[
        Recommendation(
            drug_name="Metformin",
            contraindicated=True,
            clinical_reason="eGFR too low.",
            guideline_source="KDIGO 2024",
            guideline_strength=GuidelineStrength.STRONG,
            depends_on_evidence=["eGFR"],
        )
    ],
)

outputs = {
    SpecialistType.CARDIOLOGY: cardiology,
    SpecialistType.NEPHROLOGY: nephrology,
}

conflicts = detect_conflicts(outputs)

print(conflicts)